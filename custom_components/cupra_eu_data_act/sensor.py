"""Sensor platform: curated sensors + raw diagnostic data points."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import EudaConfigEntry
from .const import raw_unique_id
from .coordinator import EudaCoordinator
from .data import (
    CURATED_BINARY_DOTTED,
    CURATED_BINARY_FLAT,
    CURATED_SENSORS_DOTTED,
    CURATED_SENSORS_FLAT,
    UNIT_RESOLVERS,
    CuratedSensor,
    DataPoint,
    detect_dataset_format,
    find_by_field,
    friendly_name,
    is_sentinel,
    resolve_distance_unit,
)
from .entity import EudaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EudaConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator

    # Status sensor is always present, even before the first dataset arrives,
    # so the user sees a device with a state explaining what's happening.
    async_add_entities([EudaStatusSensor(coordinator)])

    added_curated: set[str] = set()
    added_raw_keys: set[str] = set()
    # Pin the detected format after the first non-empty refresh; later
    # datasets that mix formats won't flip the chosen registry.
    format_state: dict[str, str | None] = {"format": None}

    @callback
    def _discover() -> None:
        points: dict[str, DataPoint] = coordinator.data or {}
        if not points:
            return

        if format_state["format"] is None:
            format_state["format"] = detect_dataset_format(points)
        format_type = format_state["format"]

        curated_sensors = (
            CURATED_SENSORS_DOTTED if format_type == "dotted" else CURATED_SENSORS_FLAT
        )
        curated_binary = (
            CURATED_BINARY_DOTTED if format_type == "dotted" else CURATED_BINARY_FLAT
        )
        binary_fields = {b.field_name for b in curated_binary}
        curated_sensor_fields = {s.field_name for s in curated_sensors}
        present_fields = {dp.field_name for dp in points.values()}

        new_entities: list[SensorEntity] = []

        for curated in curated_sensors:
            if curated.field_name in added_curated:
                continue
            # Timestamp sensors track ".timestamp" on a base field (e.g.
            # mileage.value.timestamp). They appear once the base field arrives.
            if ".timestamp" in curated.field_name:
                base_field = curated.field_name.replace(".timestamp", "")
                if base_field in present_fields:
                    new_entities.append(EudaCuratedSensor(coordinator, curated))
                    added_curated.add(curated.field_name)
            elif curated.field_name in present_fields:
                new_entities.append(EudaCuratedSensor(coordinator, curated))
                added_curated.add(curated.field_name)

        for key, dp in points.items():
            if key in added_raw_keys:
                continue
            if dp.field_name in curated_sensor_fields or dp.field_name in binary_fields:
                continue
            new_entities.append(EudaRawSensor(coordinator, key))
            added_raw_keys.add(key)

        if new_entities:
            async_add_entities(new_entities)

    _discover()
    entry.async_on_unload(coordinator.async_add_listener(_discover))


class EudaCuratedSensor(EudaEntity, SensorEntity):
    """A curated, well-typed sensor (enabled by default)."""

    def __init__(self, coordinator: EudaCoordinator, curated: CuratedSensor) -> None:
        super().__init__(coordinator)
        self._curated = curated
        self._attr_unique_id = f"{coordinator.vin}_{curated.field_name}"
        self._attr_name = curated.name
        if curated.icon:
            self._attr_icon = curated.icon
        if curated.device_class:
            self._attr_device_class = SensorDeviceClass(curated.device_class)
        if curated.state_class:
            self._attr_state_class = SensorStateClass(curated.state_class)
        if curated.suggested_display_precision is not None:
            self._attr_suggested_display_precision = curated.suggested_display_precision

    def _apply_transform(self, value):
        """Apply configured transform to the raw value."""
        if value is None or not self._curated.transform:
            return value

        transform = self._curated.transform

        if transform == "duration_s":
            # Already handled by parse_duration_seconds in parse_value
            return value

        if transform == "decikelvin_to_celsius":
            from .data import decikelvin_to_celsius

            return decikelvin_to_celsius(str(value))

        return value

    @property
    def native_value(self):
        # Special handling for timestamp fields (both "mileage.timestamp" and "mileage.value.timestamp")
        if ".timestamp" in self._curated.field_name:
            base_field = self._curated.field_name.replace(".timestamp", "")
            dp = find_by_field(self.coordinator.data or {}, base_field)
            if dp and dp.timestamp:
                return self._sticky(dp.timestamp)
            return self._sticky(None)

        field_name = self._curated.field_name
        dp = find_by_field(self.coordinator.data or {}, field_name)

        if not dp:
            return self._sticky(None)

        # Sentinels are filtered against the raw portal value (before
        # transforms) so e.g. fuel-consumption /10 doesn't turn 4294967295
        # into a "plausible" 429496729.5.
        if is_sentinel(dp.value, field_name):
            return self._sticky(None)

        raw_value = dp.value

        # Apply transforms if specified
        if self._curated.transform:
            if self._curated.transform == "decikelvin_to_celsius":
                from .data import decikelvin_to_celsius

                transformed = decikelvin_to_celsius(dp.raw_value)
                return self._sticky(transformed)

            elif self._curated.transform == "abs":
                from .data import abs_value

                transformed = abs_value(raw_value)
                return self._sticky(transformed)

            elif self._curated.transform == "fuel_consumption":
                from .data import fuel_consumption_l_per_1000km_to_l_per_100km

                transformed = fuel_consumption_l_per_1000km_to_l_per_100km(raw_value)
                return self._sticky(transformed)

            elif self._curated.transform == "electr_consumption":
                from .data import electr_consumption_kwh_per_1000km_to_kwh_per_100km

                transformed = electr_consumption_kwh_per_1000km_to_kwh_per_100km(
                    raw_value
                )
                return self._sticky(transformed)

            elif self._curated.transform == "deci_kwh":
                from .data import deci_kwh_to_kwh

                transformed = deci_kwh_to_kwh(raw_value)
                return self._sticky(transformed)

        return self._sticky(raw_value)

    @property
    def native_unit_of_measurement(self) -> str | None:
        # When a companion unit field is declared (e.g. mileage.unit), resolve
        # the unit at runtime so miles vs km is reported correctly per vehicle;
        # otherwise use the static curated unit.
        cur = self._curated
        if cur.unit_field:
            dp = find_by_field(self.coordinator.data or {}, cur.unit_field)
            if dp is not None:
                resolver = UNIT_RESOLVERS.get(cur.unit_resolver, resolve_distance_unit)
                resolved = resolver(dp.value)
                if resolved:
                    return resolved
        return cur.unit


class EudaRawSensor(EudaEntity, SensorEntity):
    """A raw data point exposed as a disabled-by-default diagnostic sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, coordinator: EudaCoordinator, key: str) -> None:
        super().__init__(coordinator)
        dp = coordinator.data[key]
        self._key = key
        # Namespace by VIN: dataset keys are shared across vehicles, so a bare
        # key collides between config entries (see raw_unique_id / migration).
        self._attr_unique_id = raw_unique_id(coordinator.vin, key)
        self._attr_name = friendly_name(dp.field_name, dp.description)
        # only attach a unit when the value is numeric
        if dp.field_name == "value_of_the_primary_range":
            self._attr_native_unit_of_measurement = "km"
            self._attr_device_class = SensorDeviceClass.DISTANCE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif dp.unit and dp.type_hint in ("int", "float"):
            self._attr_native_unit_of_measurement = dp.unit

    @property
    def native_value(self):
        dp = (self.coordinator.data or {}).get(self._key)
        if not dp:
            return self._sticky(None)
        return self._filtered(dp.value, dp.field_name)

    @property
    def extra_state_attributes(self) -> dict:
        dp = (self.coordinator.data or {}).get(self._key)
        if not dp:
            return {}
        attrs = {"key": dp.key, "field_name": dp.field_name}
        if dp.description:
            attrs["description"] = dp.description
        if dp.cluster:
            attrs["cluster"] = dp.cluster
        return attrs


class EudaStatusSensor(EudaEntity, SensorEntity):
    """Always-present diagnostic sensor showing the integration's portal state.

    Created at setup so the device exists in HA even before the first dataset
    arrives, with a state that tells the user why their other entities haven't
    appeared yet.
    """

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:cloud-sync-outline"

    def __init__(self, coordinator: EudaCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.vin}_integration_status"
        self._attr_name = "Integration status"

    @property
    def available(self) -> bool:
        return True

    @property
    def native_value(self) -> str | None:
        return self.coordinator.status_label

    @property
    def extra_state_attributes(self) -> dict:
        attrs: dict = {
            "empty_snapshot_count": self.coordinator.empty_snapshot_count,
        }
        if self.coordinator.latest_dataset and self.coordinator.latest_dataset.captured_at:
            attrs["latest_dataset_captured_at"] = (
                self.coordinator.latest_dataset.captured_at.isoformat()
            )
        return attrs
