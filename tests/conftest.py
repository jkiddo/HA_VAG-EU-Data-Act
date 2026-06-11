"""Shared fixtures for the HA-harness tests."""
from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Allow HA to load the bundled custom integration during tests."""
    yield
