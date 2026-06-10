"""VW Group brand registry for EU Data Act OIDC login.

Each brand uses the same portal and API paths but a different OIDC client_id
and state suffix. Mappings verified against the portal login selector and
documented in evcc (MIT) and ioBroker.vw-connect (MIT).
"""
from __future__ import annotations

from dataclasses import dataclass

from .const import DEFAULT_COUNTRY, DEFAULT_LANGUAGE


@dataclass(frozen=True)
class BrandConfig:
    """OIDC and display settings for one VW Group brand."""

    slug: str
    oidc_state_key: str
    title: str
    manufacturer: str
    client_id: str

    def oidc_state(self, country: str = DEFAULT_COUNTRY, language: str = DEFAULT_LANGUAGE) -> str:
        return f"{country}__{language}__{self.oidc_state_key}"


BRANDS: tuple[BrandConfig, ...] = (
    BrandConfig(
        slug="volkswagen",
        oidc_state_key="VOLKSWAGEN_PASSENGER_CARS",
        title="Volkswagen",
        manufacturer="Volkswagen",
        client_id="9b58543e-1c15-4193-91d5-8a14145bebb0@apps_vw-dilab_com",
    ),
    BrandConfig(
        slug="volkswagen_commercial",
        oidc_state_key="VOLKSWAGEN_COMMERCIAL_VEHICLES",
        title="Volkswagen Commercial Vehicles",
        manufacturer="Volkswagen",
        client_id="9b58543e-1c15-4193-91d5-8a14145bebb0@apps_vw-dilab_com",
    ),
    BrandConfig(
        slug="audi",
        oidc_state_key="AUDI",
        title="Audi",
        manufacturer="Audi",
        client_id="cc29b87a-5e9a-4362-aecf-5adea6b01bbb@apps_vw-dilab_com",
    ),
    BrandConfig(
        slug="skoda",
        oidc_state_key="SKODA",
        title="Škoda",
        manufacturer="Škoda",
        client_id="3ea88bf9-1d4e-4a68-b3ad-4098c1f1d246@apps_vw-dilab_com",
    ),
    BrandConfig(
        slug="seat",
        oidc_state_key="SEAT",
        title="SEAT",
        manufacturer="SEAT",
        client_id="f85e5b69-e3b2-43aa-9c0d-1b7d0e0b576f@apps_vw-dilab_com",
    ),
    BrandConfig(
        slug="cupra",
        oidc_state_key="CUPRA",
        title="Cupra",
        manufacturer="Cupra",
        client_id="f85e5b69-e3b2-43aa-9c0d-1b7d0e0b576f@apps_vw-dilab_com",
    ),
    BrandConfig(
        slug="bentley",
        oidc_state_key="BENTLEY",
        title="Bentley",
        manufacturer="Bentley",
        client_id="d38aac0f-3d89-4a63-8538-b75b31322c7b@apps_vw-dilab_com",
    ),
)

_BRAND_BY_SLUG = {b.slug: b for b in BRANDS}

# Existing installs created before multi-brand support default to Cupra.
DEFAULT_BRAND = "cupra"


def get_brand(slug: str) -> BrandConfig:
    """Return brand config for a config-entry slug."""
    try:
        return _BRAND_BY_SLUG[slug]
    except KeyError as err:
        raise ValueError(f"Unknown brand {slug!r}") from err


def brand_options() -> list[tuple[str, str]]:
    """(slug, title) pairs for config-flow selectors."""
    return [(b.slug, b.title) for b in BRANDS]
