"""Load integration modules without Home Assistant (for offline tests)."""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "custom_components" / "cupra_eu_data_act"
PKG = "cupra_eu_data_act"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_modules(*names: str) -> dict:
    """Import ``const``, ``data``, ``api``, … from the custom component tree."""
    if PKG not in sys.modules:
        pkg = types.ModuleType(PKG)
        pkg.__path__ = [str(PKG_DIR)]
        sys.modules[PKG] = pkg
    mods = {}
    for name in names:
        key = f"{PKG}.{name}"
        if key in sys.modules:
            mods[name] = sys.modules[key]
            continue
        spec = importlib.util.spec_from_file_location(key, PKG_DIR / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = PKG
        sys.modules[key] = mod
        spec.loader.exec_module(mod)
        mods[name] = mod
    return mods
