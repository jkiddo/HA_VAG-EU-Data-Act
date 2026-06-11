"""Base entity for the VW Group EU Data Act integration."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .brands import DEFAULT_BRAND, get_brand
from .const import CONF_BRAND, CONF_NICKNAME, DOMAIN
from .coordinator import EudaCoordinator
from .data import is_sentinel, sticky


class EudaEntity(CoordinatorEntity[EudaCoordinator]):
    """Common base: shares one device per VIN."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: EudaCoordinator) -> None:
        super().__init__(coordinator)
        self._last_value = None
        vin = coordinator.vin
        name = coordinator.entry.data.get(CONF_NICKNAME) or vin
        brand = get_brand(coordinator.entry.data.get(CONF_BRAND, DEFAULT_BRAND))
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, vin)},
            name=name,
            manufacturer=brand.manufacturer,
            model="EU Data Act vehicle",
            serial_number=vin,
        )

    @property
    def available(self) -> bool:
        """Stay available across transient poll failures.

        The portal only publishes a new dataset every ~15 min and we keep the
        last one, so a failed refresh (e.g. a transient DNS/network blip) should
        keep showing the last known values rather than flipping every entity to
        "unavailable". We only report unavailable until the first dataset has
        ever loaded.
        """
        return self.coordinator.data is not None

    def _sticky(self, value):
        """Return ``value``, or the last known value if this update omits it."""
        self._last_value = sticky(self._last_value, value)
        return self._last_value

    def _filtered(self, value, field_name: str | None = None):
        """Drop portal sentinels then apply sticky semantics.

        Sentinel values (e.g. uint32-max mileage) are treated the same as a
        missing field: the last known value is kept rather than recording the
        garbage reading. When no previous value exists, ``None`` propagates so
        the entity reports ``unknown`` until real data arrives.
        """
        if is_sentinel(value, field_name):
            return self._sticky(None)
        return self._sticky(value)
