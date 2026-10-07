from playwright.sync_api import Locator, Page

from saucedemo.pages.base_page import BasePage
from saucedemo.pages.checkout_page import CheckoutInfoPage
from saucedemo.pages.components import Header


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = Header(page)
        self.cart_list = page.get_by_test_id("cart-list")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")

    @property
    def loaded_marker(self) -> Locator:
        return self.cart_list

    def get_item_names(self) -> list[str]:
        return [name.strip() for name in self.item_names.all_inner_texts()]

    def checkout(self) -> CheckoutInfoPage:
        self.click(self.checkout_button, "Checkout")
        return CheckoutInfoPage(self.page).wait_until_loaded()
