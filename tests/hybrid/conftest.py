"""Hybrid tests start authenticated, optionally with a pre-filled cart.

Usage:
    @pytest.mark.cart("Sauce Labs Backpack", "Sauce Labs Bike Light")
    def test_something(page): ...
"""

from typing import Any

import pytest
from playwright.sync_api import Page

from saucedemo.config import Settings
from saucedemo.data import get_product
from saucedemo.models import User
from saucedemo.pages import InventoryPage
from saucedemo.utils.session import build_storage_state


@pytest.fixture
def context_options(
    context_options: dict[str, Any],
    settings: Settings,
    standard_user: User,
    request: pytest.FixtureRequest,
) -> dict[str, Any]:
    """Extends the root options with a session cookie and cart state from @pytest.mark.cart."""
    cart_marker = request.node.get_closest_marker("cart")
    cart_names = cart_marker.args if cart_marker else ()
    storage_state = build_storage_state(
        base_url=settings.base_url,
        username=standard_user.username,
        cart_product_ids=[get_product(name).id for name in cart_names],
    )
    return {**context_options, "storage_state": storage_state}


@pytest.fixture
def fast_inventory_page(page: Page) -> InventoryPage:
    """Inventory opened directly, no login form involved."""
    return InventoryPage(page).open()
