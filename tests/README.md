# Tests

Two layers, run independently.

## Offline core tests (no Home Assistant)

`test_offline.py`, `test_api_mock.py`, `test_brands.py` exercise the pure-Python
pieces (data parsing, transforms, sentinel detection, binary decoding, brand
registry, login HTML parsing). They depend only on `aiohttp` and run on the
project's regular Python venv:

```bash
python tests/test_offline.py
python tests/test_api_mock.py
python tests/test_brands.py
```

These are the fast feedback loop for refactors that don't touch Home Assistant.

## HA-harness tests (full Home Assistant)

`test_coordinator.py` and `test_config_flow.py` use
[`pytest-homeassistant-custom-component`](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component)
to spin up a real `hass` instance and load the integration the same way Home
Assistant does at runtime. They cover the two things you can't test offline:

- Authentication failures must surface as `ConfigEntryAuthFailed` so HA shows
  the reauth dialog, not as a silent retry.
- The reauth step must restore `CONF_BRAND` from the stored entry so non-VW
  users (Škoda, Cupra, …) log in against the right OIDC client.

Install and run from a Python 3.13+ venv:

```bash
pip install -r requirements_test.txt
pytest tests/test_coordinator.py tests/test_config_flow.py -v
```

On Windows, run the harness from WSL or a Linux container — HA's test
dependencies (`uvloop`, native bluetooth bindings) don't build on native
Windows. The offline tests work everywhere.
