import re

import allure
import pytest
from playwright.sync_api import Page, expect

from saucedemo.data import get_product, load_products
from saucedemo.models import Customer, Product
from saucedemo.pages import CartPage, InventoryPage

pytestmark = [pytest.mark.hybrid, allure.epic("SauceDemo"), allure.feature("Session injection")]

CART_PRODUCTS = ("Sauce Labs Backpack", "Sauce Labs Fleece Jacket")


@pytest.mark.smoke
@allure.title("Injected session opens the inventory without the login form")
def test_injected_session_skips_login(fast_inventory_page: InventoryPage) -> None:
    expect(fast_inventory_page.page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(fast_inventory_page.title).to_have_text("Products")


@pytest.mark.regression
@pytest.mark.cart(*CART_PRODUCTS)
@allure.story("Purchase")
@allure.title("Checkout with a cart pre-filled via localStorage")
def test_checkout_with_prefilled_cart(page: Page, customer: Customer) -> None:
    expected = [get_product(name) for name in CART_PRODUCTS]

    cart = CartPage(page).open()
    expect(cart.header.cart_badge).to_have_text(str(len(expected)))
    assert cart.get_item_names() == list(CART_PRODUCTS)

    overview = cart.checkout().fill_info(customer).continue_to_overview()
    summary = overview.get_summary()
    assert summary.subtotal == sum(product.price for product in expected)
    assert summary.total == summary.subtotal + summary.tax

    complete = overview.finish()
    expect(complete.complete_header).to_have_text("Thank you for your order!")


@pytest.mark.regression
@allure.title("Catalog data matches the UI: {product.name}")
@pytest.mark.parametrize("product", load_products(), ids=lambda product: product.name)
def test_catalog_matches_ui(fast_inventory_page: InventoryPage, product: Product) -> None:
    assert fast_inventory_page.get_product(product.name) == product
