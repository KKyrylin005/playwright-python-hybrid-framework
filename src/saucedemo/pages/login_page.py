from typing import Self

import allure
from playwright.sync_api import Locator, Page

from saucedemo.models import User
from saucedemo.pages.base_page import BasePage
from saucedemo.pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    @property
    def loaded_marker(self) -> Locator:
        return self.login_button

    def submit_credentials(self, username: str, password: str) -> Self:
        """Low-level action: stays on this page, so it fits negative scenarios."""
        self.fill(self.username_input, username, "Username")
        self.fill(self.password_input, password, "Password", secret=True)
        self.click(self.login_button, "Login")
        return self

    def login(self, user: User) -> InventoryPage:
        """Happy path: returns the next page once it is loaded."""
        with allure.step(f"Log in as '{user.username}'"):
            self.submit_credentials(user.username, user.password)
        return InventoryPage(self.page).wait_until_loaded()
