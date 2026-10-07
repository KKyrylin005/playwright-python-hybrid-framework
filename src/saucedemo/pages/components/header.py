"""Header shared by all authorised pages (composition, not inheritance)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page, expect

if TYPE_CHECKING:
    from saucedemo.pages.cart_page import CartPage
    from saucedemo.pages.login_page import LoginPage


class Header:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")

    def open_cart(self) -> CartPage:
        # Local import breaks the cycle: pages own a Header, Header navigates to pages
        from saucedemo.pages.cart_page import CartPage

        with allure.step("Open cart from header"):
            self.cart_link.click()
        return CartPage(self.page).wait_until_loaded()

    def logout(self) -> LoginPage:
        from saucedemo.pages.login_page import LoginPage

        with allure.step("Log out via side menu"):
            self.menu_button.click()
            expect(self.logout_link).to_be_visible()  # menu slides in with an animation
            self.logout_link.click()
        return LoginPage(self.page).wait_until_loaded()
