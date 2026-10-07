"""Three checkout steps: shipping info -> overview -> complete."""

from typing import Self

import allure
from playwright.sync_api import Locator, Page

from saucedemo.models import Customer, OrderSummary
from saucedemo.pages.base_page import BasePage
from saucedemo.pages.components import Header
from saucedemo.utils.money import parse_price


class CheckoutInfoPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name_input = page.get_by_test_id("firstName")
        self.last_name_input = page.get_by_test_id("lastName")
        self.postal_code_input = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.error_message = page.get_by_test_id("error")

    @property
    def loaded_marker(self) -> Locator:
        return self.continue_button

    def fill_info(self, customer: Customer) -> Self:
        with allure.step(f"Fill shipping info for '{customer.first_name} {customer.last_name}'"):
            self.fill(self.first_name_input, customer.first_name, "First Name")
            self.fill(self.last_name_input, customer.last_name, "Last Name")
            self.fill(self.postal_code_input, customer.postal_code, "Postal Code")
        return self

    def continue_to_overview(self) -> "CheckoutOverviewPage":
        self.click(self.continue_button, "Continue")
        return CheckoutOverviewPage(self.page).wait_until_loaded()


class CheckoutOverviewPage(BasePage):
    path = "/checkout-step-two.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.subtotal_label = page.get_by_test_id("subtotal-label")
        self.tax_label = page.get_by_test_id("tax-label")
        self.total_label = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")

    @property
    def loaded_marker(self) -> Locator:
        return self.finish_button

    def get_summary(self) -> OrderSummary:
        return OrderSummary(
            subtotal=parse_price(self.get_text(self.subtotal_label)),
            tax=parse_price(self.get_text(self.tax_label)),
            total=parse_price(self.get_text(self.total_label)),
        )

    def finish(self) -> "CheckoutCompletePage":
        self.click(self.finish_button, "Finish")
        return CheckoutCompletePage(self.page).wait_until_loaded()


class CheckoutCompletePage(BasePage):
    path = "/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = Header(page)
        self.complete_header = page.get_by_test_id("complete-header")
        self.back_home_button = page.get_by_test_id("back-to-products")

    @property
    def loaded_marker(self) -> Locator:
        return self.complete_header
