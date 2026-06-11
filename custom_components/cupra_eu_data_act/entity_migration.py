"""Entity registry migrations for translation_key / naming fixes."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er

from .const import CONF_VIN
from .data import (
    CURATED_BINARY_DOTTED,
    CURATED_BINARY_FLAT,
    CURATED_SENSORS_DOTTED,
    CURATED_SENSORS_FLAT,
    curated_translation_key,
)

_FIELD_TO_TRANSLATION_KEY: dict[str, str] = {
    s.field_name: curated_translation_key(s.field_name, s.translation_key)
    for s in (*CURATED_SENSORS_DOTTED, *CURATED_SENSORS_FLAT)
}
_BINARY_FIELD_TO_TRANSLATION_KEY: dict[str, str] = {
    b.field_name: curated_translation_key(b.field_name)
    for b in (*CURATED_BINARY_DOTTED, *CURATED_BINARY_FLAT)
}


def translation_key_for_unique_id(unique_id: str, vin: str) -> str | None:
    """Map a curated sensor unique_id to its HA translation_key."""
    if unique_id == f"{vin}_integration_status":
        return "integration_status"
    for suffix, key in (
        ("days_until_subscription_expires", "days_until_subscription_expires"),
        ("minutes_since_last_snapshot", "minutes_since_last_snapshot"),
        ("last_vehicle_update", "last_vehicle_update"),
        ("dataset_generated", "dataset_generated"),
        ("uncurated_fields_count", "uncurated_fields_count"),
    ):
        if unique_id == f"{vin}_{suffix}":
            return key
    prefix = f"{vin}_"
    if not unique_id.startswith(prefix):
        return None
    field = unique_id[len(prefix) :]
    return _FIELD_TO_TRANSLATION_KEY.get(field) or _BINARY_FIELD_TO_TRANSLATION_KEY.get(
        field
    )


async def async_migrate_entity_translations(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Ensure curated entities use translation_key instead of stale registry names.

    Curated sensors and binary sensors must not set ``_attr_name`` (especially not
    to ``None`` — that tells HA to use the device name only). Existing registry
    entries created before localization may lack ``translation_key`` or still carry
    a custom ``name`` override.
    """
    vin = entry.data[CONF_VIN]

    @callback
    def _migrate(reg_entry: er.RegistryEntry) -> dict | None:
        if reg_entry.domain not in ("sensor", "binary_sensor"):
            return None
        key = translation_key_for_unique_id(reg_entry.unique_id, vin)
        if not key:
            return None
        if reg_entry.translation_key == key and reg_entry.name is None:
            return None
        return {"translation_key": key, "name": None}

    await er.async_migrate_entries(hass, entry.entry_id, _migrate)
