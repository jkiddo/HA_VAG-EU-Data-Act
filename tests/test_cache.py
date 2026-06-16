#!/usr/bin/env python3
"""Offline tests for the local dataset ZIP cache."""

from __future__ import annotations

import io
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

from _loader import load_modules  # noqa: E402

cache_mod = load_modules("cache")["cache"]
DatasetCache = cache_mod.DatasetCache
vin_cache_key = cache_mod.vin_cache_key


def _make_zip(name: str = "data.json", payload: bytes = b"{}") -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(name, payload)
    return buf.getvalue()


def main() -> int:
    failed = 0
    tmp = Path(__file__).parent / ".cache_test_tmp"
    tmp.mkdir(exist_ok=True)

    def check(label: str, got, expected) -> None:
        nonlocal failed
        ok = got == expected
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {got!r}")
        if not ok:
            failed += 1

    vin = "WVWZZZTESTVIN0001"
    cache = DatasetCache(tmp / "cache", max_files=3, max_bytes_per_vin=10_000)

    print("vin_cache_key:")
    key = vin_cache_key(vin)
    check("16 hex chars", len(key), 16)
    check("no vin substring", vin in key, False)

    print("store and list:")
    cache.store(vin, "a_20260101000000.zip", _make_zip())
    cache.store(vin, "b_20260102000000.zip", _make_zip())
    entries = cache.list_entries(vin)
    check("two files", len(entries), 2)
    check("newest first name", entries[0].name, "b_20260102000000.zip")

    print("rotation by count:")
    cache.store(vin, "c_20260103000000.zip", _make_zip())
    cache.store(vin, "d_20260104000000.zip", _make_zip())
    names = {e.name for e in cache.list_entries(vin)}
    check("max 3 files kept", len(names), 3)
    check("oldest dropped", "a_20260101000000.zip" in names, False)

    print("unsafe name rejected:")
    before = len(cache.list_entries(vin))
    cache.store(vin, "../evil.zip", _make_zip())
    check("no extra file", len(cache.list_entries(vin)), before)

    print("read_latest:")
    latest = cache.read_latest(vin)
    check("read_latest name", latest[0] if latest else None, "d_20260104000000.zip")
    check("read_latest bytes", bool(latest[1]) if latest else False, True)

    print("rotation by size:")
    big_cache = DatasetCache(tmp / "big", max_files=10, max_bytes_per_vin=500)
    big_cache.store(vin, "big1.zip", b"x" * 300)
    big_cache.store(vin, "big2.zip", b"y" * 300)
    remaining = {e.name for e in big_cache.list_entries(vin)}
    check("size cap drops oldest", "big1.zip" in remaining, False)
    check("newest kept", "big2.zip" in remaining, True)

    # cleanup
    import shutil

    shutil.rmtree(tmp, ignore_errors=True)

    if failed:
        print(f"\n{failed} CACHE TEST(S) FAILED")
        return 1
    print("\nALL CACHE TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
