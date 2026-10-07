import dataclasses
import re

import allure
import pytest
from playwright.sync_api import Page, expect

from saucedemo.models import Customer
from saucedemo.pages import CheckoutInfoPage

pytestmark = [
    pytest.mark.hybrid,
    pytest.mark.regression,
    # The cart is pre-filled, so each case starts directly on the checkout step
    pytest.mark.cart("Sauce Labs Backpack"),
    allure.epic("SauceDemo"),
    allure.feature("Checkout"),
    allure.story("Shipping info validation"),
]


@allure.title("Checkout is blocked when '{missing_field}' is empty")
@pytest.mark.parametrize(
    ("missing_field", "expected_error"),
    [
        pytest.param("first_name", "First Name is required", id="empty-first-name"),
        pytest.param("last_name", "Last Name is required", id="empty-last-name"),
        pytest.param("postal_code", "Postal Code is required", id="empty-postal-code"),
    ],
)
def test_checkout_requires_shipping_field(
    page: Page, customer: Customer, missing_field: str, expected_error: str
) -> None:
    incomplete = dataclasses.replace(customer, **{missing_field: ""})

    info = CheckoutInfoPage(page).open().fill_info(incomplete).continue_expecting_error()

    expect(info.error_message).to_contain_text(expected_error)
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))


@allure.title("Checkout with all shipping fields empty reports the first missing field")
def test_checkout_with_empty_form(page: Page) -> None:
    info = CheckoutInfoPage(page).open().continue_expecting_error()

    expect(info.error_message).to_contain_text("First Name is required")
