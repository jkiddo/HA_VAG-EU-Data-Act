# Testing guide (beta testers)

Thank you for helping test **VW Group EU Data Act** for Home Assistant.

## Supported brands

| Brand slug | Select in HA | Notes |
|------------|--------------|-------|
| `volkswagen` | Volkswagen | VW passenger cars |
| `volkswagen_commercial` | Volkswagen Commercial Vehicles | Crafter, etc. |
| `audi` | Audi | myAudi credentials |
| `skoda` | Škoda | MyŠkoda credentials |
| `seat` | SEAT | SEAT ID credentials |
| `cupra` | Cupra | Cupra ID / MyCupra credentials |
| `bentley` | Bentley | Bentley credentials |

**Important:** Choose the brand that matches your account. VW credentials with the Cupra brand (or vice versa) will fail login.

## Portal setup (required)

1. Log in at [eu-data-act.drivesomethinggreater.com](https://eu-data-act.drivesomethinggreater.com/)
2. Connect your vehicle under **Data clusters → Vehicle overview**
3. Create a **continuous 15-minute** data request
4. Wait for ZIP files (first real data can take one or more intervals)

## Quick smoke test (no Home Assistant)

```bash
python3 -m venv .venv && .venv/bin/pip install aiohttp

# List brands
.venv/bin/python tools/test_login.py --list-brands

# Test your brand (replace brand, email, password)
.venv/bin/python tools/test_login.py --brand audi you@example.com 'your-password'
```

| Exit code | Meaning |
|-----------|---------|
| `0` | Login OK + real dataset downloaded |
| `1` | Error — wrong brand/credentials or portal issue |
| `2` | Login OK, waiting for portal data (`_no_content_found` is normal at first) |

## Home Assistant installation

### HACS

Add custom repository: `https://github.com/TommiG1/HA_VAG-EU-Data-Act`  
Install **VW Group EU Data Act** → restart HA.

### Config flow

1. **Settings → Devices & Services → Add Integration**
2. Search **VW Group EU Data Act**
3. Select your **brand**, enter email/password, pick vehicle

While waiting for the first real ZIP, the integration shows as **not loaded** and retries — this is expected.

## What to report

Please open a [GitHub issue](https://github.com/TommiG1/HA_VAG-EU-Data-Act/issues) with:

- Brand slug and vehicle model (no VIN required)
- `test_login.py` exit code and last lines of output (redact email)
- HA version
- Whether portal ZIPs contain real data or only `_no_content_found`
- Relevant log lines (`custom_components.cupra_eu_data_act: debug`)

## Offline tests (for developers)

```bash
.venv/bin/python tests/test_offline.py
.venv/bin/python tests/test_api_mock.py
.venv/bin/python tests/test_brands.py
```
