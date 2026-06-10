# Release notes

## v0.2.0 — Multi-brand support (2026-06-10)

### Summary

All major VW Group brands on the EU Data Act portal are now supported in one
integration. Select your brand during setup — OIDC login uses the correct
`client_id` and state for each marque.

### Supported brands

- Volkswagen (passenger cars)
- Volkswagen Commercial Vehicles
- Audi
- Škoda
- SEAT
- Cupra
- Bentley

### Changes

- Brand selector in config flow (`CONF_BRAND` stored per vehicle)
- `brands.py` registry with per-brand OIDC parameters (from evcc / ioBroker, MIT)
- Device `manufacturer` reflects selected brand
- `tools/test_login.py --brand <slug>` and `--list-brands` for testers
- [TESTING.md](TESTING.md) guide for beta testers
- Display name renamed to **VW Group EU Data Act** (domain `cupra_eu_data_act` unchanged for compatibility)

### Upgrade notes

- Existing Cupra installs without `brand` in config default to **Cupra**
- Re-add the integration to change brand, or edit `core.config_entries` manually

### Tester checklist

```bash
.venv/bin/python tools/test_login.py --list-brands
.venv/bin/python tools/test_login.py --brand <your-brand> email password
```

Report results via GitHub issues — see [TESTING.md](TESTING.md).

---

## v0.1.2 — Initial public beta (2026-06-10)

First public release of the Cupra EU Data Act Home Assistant integration.

### Summary

This integration connects Home Assistant to the official Volkswagen Group EU Data
Act portal for Cupra vehicles. It provides read-only sensors (battery, charging,
range, mileage, lock state, and more) with roughly 15-minute update intervals.

### What's included

- **Config flow** — sign in with Cupra ID, select vehicle, automatic identifier detection
- **Curated sensors** — battery SoC, target SoC, charge power/rate, range, mileage,
  charge state/mode, temperatures, last-connected timestamp, and more
- **Binary sensors** — vehicle locked, parking brake
- **Diagnostic sensors** — optional raw data points from the official VW data dictionary
- **Adaptive polling** — refresh interval aligned with portal dataset delivery (~15 min)
- **German translations** — config flow strings in `de.json`
- **Offline test suite** — parsing, ZIP extraction, login HTML helpers, API response handling
- **CI workflow** — GitHub Actions runs tests on push and pull requests
- **Smoke-test tool** — `tools/test_login.py` for live portal verification outside HA

### Setup behaviour

- On first load, if no dataset with real content is available yet, the integration
  raises `ConfigEntryNotReady` and retries automatically instead of failing with a
  permanent setup error.
- HTTP **404** on the dataset list endpoint (no ZIPs delivered yet) is treated as
  an empty list.
- **`_no_content_found.zip`** files (empty portal snapshots) are skipped; the
  integration waits for the next interval.
- If the portal subscription is recreated, the data-request **identifier** is
  refreshed automatically from the metadata endpoint.

### Portal requirements

Users must configure a **continuous 15-minute data request** on
[eu-data-act.drivesomethinggreater.com](https://eu-data-act.drivesomethinggreater.com/)
before adding the integration in Home Assistant.

### Known limitations

- **Read-only** — no climate control, charging commands, or other vehicle actions
- **~15 minute latency** — not suitable for real-time automations
- **Portal dependency** — if the VW portal delivers only empty snapshots, no sensors
  will appear until real telemetry is available; this is outside the integration's control
- **Beta quality** — tested with real portal login and dataset listing; community
  feedback on different Cupra models is welcome

### Verifying your installation

```bash
# Offline (no credentials)
.venv/bin/python tests/test_offline.py
.venv/bin/python tests/test_api_mock.py

# Live portal check
EUDA_EMAIL='you@example.com' EUDA_PASSWORD='secret' .venv/bin/python tools/test_login.py
```

| `test_login.py` exit code | Interpretation |
|---------------------------|----------------|
| `0` | Working — real vehicle data downloaded |
| `2` | Working — waiting for portal to deliver data |
| `1` | Error — check credentials or portal status |

### Installation

**HACS:** Add `https://github.com/TommiG1/HA_VAG-EU-Data-Act` as a custom
integration repository, install **Cupra EU Data Act**, restart Home Assistant.

**Manual:** Copy `custom_components/cupra_eu_data_act` to your `config/custom_components/`
folder and restart.

### Requirements

- Home Assistant 2024.12.0+
- Cupra ID account with an active EU Data Act data subscription

### Credits

Derived from [hass-vw-eu-data-act](https://github.com/mikrohard/hass-vw-eu-data-act)
(MIT) by Jernej Fijačko, adapted for Cupra OIDC and branding.

API behaviour informed by MIT-licensed projects [evcc](https://github.com/evcc-io/evcc)
and [ioBroker.vw-connect](https://github.com/TA2k/ioBroker.vw-connect).

---

## Upgrade notes

This is the first release. No upgrade path from a previous version.
