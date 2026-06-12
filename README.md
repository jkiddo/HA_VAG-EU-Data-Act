# VW Group EU Data Act for Home Assistant

<p align="center">
  <img src="custom_components/cupra_eu_data_act/brand/icon.png" alt="VW Group EU Data Act" width="128" height="128">
</p>

[![Test](https://github.com/TommiG1/HA_VAG-EU-Data-Act/actions/workflows/test.yml/badge.svg)](https://github.com/TommiG1/HA_VAG-EU-Data-Act/actions/workflows/test.yml)
[![Home Assistant Community](https://img.shields.io/badge/Forum-Home%20Assistant-41BDF5?logo=homeassistant&logoColor=white)](https://community.home-assistant.io/t/beta-vw-group-eu-data-act-vehicle-data-for-vw-audi-skoda-seat-cupra-bentley-official-portal/1013514)
[![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal&logoColor=white)](https://www.paypal.com/paypalme/tommigraf)

A Home Assistant custom integration that reads vehicle data from the official
[Volkswagen Group EU Data Act portal](https://eu-data-act.drivesomethinggreater.com/).

Supports **all major VAG brands** on the portal: Volkswagen, Audi, Škoda, SEAT,
Cupra, Bentley, and Volkswagen Commercial Vehicles.

After VW restricted unofficial third-party API access in 2026, this integration
provides a **legal, read-only** alternative using the portal intended for vehicle
owners under the EU Data Act.

> **Beta** — see [TESTING.md](TESTING.md) if you want to help test your brand.
> See [RELEASE_NOTES.md](RELEASE_NOTES.md) for version history.

> **Not a replacement for WeConnect integrations:** no climate control, no
> charging commands, no real-time polling. Data updates roughly every 15 minutes.

## Supported brands

| Home Assistant | Brand slug (`test_login.py`) |
|----------------|------------------------------|
| Volkswagen | `volkswagen` |
| Volkswagen Commercial Vehicles | `volkswagen_commercial` |
| Audi | `audi` |
| Škoda | `skoda` |
| SEAT | `seat` |
| Cupra | `cupra` |
| Bentley | `bentley` |

Use the brand that matches your account credentials (VW ID, myAudi, Cupra ID, etc.).

## Requirements

- Home Assistant **2024.12.0** or newer
- Account for your brand on the EU Data Act portal
- Active **continuous 15-minute** data request on the portal

## Portal setup (required)

1. Open [eu-data-act.drivesomethinggreater.com](https://eu-data-act.drivesomethinggreater.com/)
2. Sign in and connect your vehicle under **Data clusters → Vehicle overview**
3. Create a **continuous** data request with **15-minute** frequency
4. When choosing the dataset, select **All Data** — not only **Charging**. A charging-only request delivers far fewer fields (battery, range, mileage, and many other sensors need the full dataset).
5. Wait until ZIP files with real content appear

## Installation

### HACS

1. HACS → **⋮** → **Custom repositories**
2. Add `https://github.com/TommiG1/HA_VAG-EU-Data-Act` as type **Integration**
3. Install **VW Group EU Data Act** → restart Home Assistant

### Manual

Copy `custom_components/cupra_eu_data_act` to `config/custom_components/` and restart.

### Add the integration

**Settings → Devices & Services → Add Integration → VW Group EU Data Act**

Select brand, enter credentials, choose vehicle.

## Verifying it works

```bash
python3 -m venv .venv && .venv/bin/pip install aiohttp
.venv/bin/python tests/test_offline.py
.venv/bin/python tests/test_brands.py
.venv/bin/python tools/test_login.py --brand cupra you@example.com 'secret'
```

| `test_login.py` exit | Meaning |
|----------------------|---------|
| `0` | End-to-end OK with real data |
| `2` | Login OK, waiting for portal ZIPs |
| `1` | Error — check brand and credentials |

Full tester guide: [TESTING.md](TESTING.md)

## Energy dashboard helpers

For Home Assistant Energy dashboard, use the cumulative charged-energy sensor
from this integration (it has `device_class: energy` and
`state_class: total_increasing`):

- ID.x / dotted datasets: `sensor.<vehicle>_charged_energy`
- Flat datasets (older portal layout): `sensor.<vehicle>_total_energy_charged`

The integration also auto-creates monthly `utility_meter` helpers (if missing)
for:

- monthly charged energy (kWh)
- monthly mileage (km/mi, based on your vehicle unit)
- monthly electric consumption (optional; only when a curated source exists)

Additionally, `sensor.<vehicle>_last_charge` exposes the last observed charging
delta in kWh, derived from cumulative charged-energy updates.

## Lovelace / Dashboard

Entity IDs vary by device nickname, HA language, and dataset format — this
integration does not ship copy-paste dashboard YAML. See
[`dashboards/README.md`](dashboards/README.md) for which entities are worth
adding to your own dashboard (UI entity picker or Mushroom Cards via HACS).

## Limitations

- Read-only, ~15 min latency, portal-dependent delivery
- `_no_content_found.zip` empty snapshots are skipped automatically
- Porsche is not on this portal
- Intended for persons living in the **EU(27)** with vehicles **registered in the EU(27)**. Users outside the EU (e.g. Switzerland) may register on the portal but often receive no actual data delivery

## Support

Questions, feedback, and beta testing: [Home Assistant Community thread](https://community.home-assistant.io/t/beta-vw-group-eu-data-act-vehicle-data-for-vw-audi-skoda-seat-cupra-bentley-official-portal/1013514)

If this integration saves you time, you can donate via PayPal:

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/paypalme/tommigraf)

[paypal.com/paypalme/tommigraf](https://www.paypal.com/paypalme/tommigraf)

## License

MIT — see [LICENSE](LICENSE). Attributions: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
