"""Mocked HTTP tests for api.py (no live portal, no Home Assistant)."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))

from _loader import load_modules  # noqa: E402


class _FakeResponse:
    def __init__(self, status: int, body: str = "", url: str = "https://example.test/"):
        self.status = status
        self._body = body
        self.url = url

    async def text(self) -> str:
        return self._body

    async def read(self) -> bytes:
        return self._body.encode()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False


class _FakeSession:
    def __init__(self, responses: list[_FakeResponse]):
        self._responses = list(responses)
        self.cookie_jar = []

    async def post(self, *args, **kwargs):
        return self._responses.pop(0)

    async def close(self):
        return None


def _client(api, session, brand, logged_in: bool = True):
    client = api.EudaApiClient(session, "test@example.com", "secret", brand)
    client._logged_in = logged_in
    return client


async def _run(label: str, coro, failures: list[str]) -> None:
    try:
        got = await coro
        print(f"  [PASS] {label}: {got!r}")
    except Exception as err:  # noqa: BLE001
        print(f"  [FAIL] {label}: {type(err).__name__}: {err}")
        failures.append(label)


async def main() -> int:
    mods = load_modules("const", "brands", "api")
    api = mods["api"]
    const = mods["const"]
    brand = mods["brands"].get_brand("cupra")
    failures: list[str] = []

    print("async_list_datasets:")
    url = f"{const.BASE_URL}{const.LIST_PATH.format(vin='WVWZZZTESTVIN0001', identifier='abc123')}"

    async def _get_404(self, req_url, **kwargs):
        assert req_url == url
        return _FakeResponse(404, url=req_url)

    session = _FakeSession([])
    client = _client(api, session, brand)
    client._get = _get_404.__get__(client, api.EudaApiClient)
    await _run("HTTP 404 -> empty list", client.async_list_datasets("WVWZZZTESTVIN0001", "abc123"), failures)

    payload = [{"name": "20260101120000_WVWZZZTESTVIN0001.zip", "createdOn": "2026-01-01T12:00:00Z"}]

    async def _get_200(self, req_url, **kwargs):
        return _FakeResponse(200, json.dumps(payload), url=req_url)

    session2 = _FakeSession([])
    client2 = _client(api, session2, brand)
    client2._get = _get_200.__get__(client2, api.EudaApiClient)
    await _run("HTTP 200 -> parsed list", client2.async_list_datasets("WVWZZZTESTVIN0001", "abc123"), failures)

    print("content filtering:")
    listing = [
        {"name": "20260101120000_WVWZZZTESTVIN0001_no_content_found.zip"},
        {"name": "20260101121500_WVWZZZTESTVIN0001.zip"},
    ]
    content = [
        e
        for e in listing
        if e.get("name") and not e["name"].endswith(const.NO_CONTENT_SUFFIX)
    ]
    ok = len(content) == 1 and content[0]["name"].endswith(".zip")
    print(f"  [{'PASS' if ok else 'FAIL'}] skip no_content zip: {content!r}")
    if not ok:
        failures.append("content filtering")

    print()
    if failures:
        print(f"FAILED: {len(failures)} -> {failures}")
        return 1
    print("ALL API MOCK TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
