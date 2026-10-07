import allure
import pytest
from playwright.sync_api import expect

from saucedemo.models import Customer
from saucedemo.pages import InventoryPage

pytestmark = [pytest.mark.ui, allure.epic("SauceDemo"), allure.feature("Checkout")]

PRODUCT_NAMES = ("Sauce Labs Backpack", "Sauce Labs Bike Light")


@pytest.mark.smoke
@allure.story("Purchase")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Standard user buys two products end to end")
def test_purchase_two_products(inventory_page: InventoryPage, customer: Customer) -> None:
    with allure.step("Add products to the cart"):
        products = [inventory_page.get_product(name) for name in PRODUCT_NAMES]
        inventory_page.add_to_cart(*PRODUCT_NAMES)
        expect(inventory_page.header.cart_badge).to_have_text(str(len(products)))

    with allure.step("Verify cart contents"):
        cart = inventory_page.header.open_cart()
        assert cart.get_item_names() == list(PRODUCT_NAMES)

    with allure.step("Verify order totals on the overview"):
        overview = cart.checkout().fill_info(customer).continue_to_overview()
        summary = overview.get_summary()
        assert summary.subtotal == sum(product.price for product in products)
        assert summary.total == summary.subtotal + summary.tax

    with allure.step("Finish the order"):
        complete = overview.finish()
        expect(complete.complete_header).to_have_text("Thank you for your order!")
        expect(complete.header.cart_badge).to_be_hidden()
