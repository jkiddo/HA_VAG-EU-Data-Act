# Lovelace / Dashboard

This integration does **not** ship ready-made dashboard YAML files.

Entity IDs depend on device nickname, HA language, and dataset format (dotted vs.
flat) — a copy-paste template would not fit most installations.

## Finding entities

1. **Settings → Devices & services** → open your vehicle device
2. Or **Developer tools → States** and filter by your device slug
3. Add cards in the UI (e.g. Mushroom Cards via HACS) and pick entities from the picker

## Suggested cards (by purpose)

| Purpose | Type | Notes |
|---------|------|-------|
| Battery (SOC) | `sensor` | Curated when present in the portal |
| Electric range | `sensor` | BEV/PHEV; ID.7 may use `value_of_the_primary_range` |
| Charge state / power / target | `sensor` | Read-only — no charge commands |
| 12V battery voltage | `sensor` | PHEV / flat format (e.g. Terramar), when present |
| Mileage | `sensor` | When the portal provides it |
| Vehicle locked | `binary_sensor` | |
| Integration status | `sensor` | `integration_status` |
| Data age | `sensor` | `minutes_since_last_snapshot`; per-sensor `age_minutes` attribute on curated sensors |
| Subscription expiry | `sensor` | `days_until_subscription_expires` |
| New portal fields | `sensor` | `uncurated_fields_count` — normal if > 0 |
| Refresh now | `button` | `refresh` |

Optional (only if the entity exists): battery min/max temperature,
`last_charge_kwh` (last charging session — not available on all vehicles).

Raw diagnostic sensors (disabled by default) can be ignored for everyday use.

## Energy dashboard

See [README.md](../README.md#energy-dashboard-helpers) for cumulative energy
sensors and auto-created `utility_meter` helpers.

## Mushroom Cards

If you use Mushroom: add cards in the visual editor and select entities from the
picker. An `icon_color` per card is enough for a clean layout — no fixed YAML
required.
