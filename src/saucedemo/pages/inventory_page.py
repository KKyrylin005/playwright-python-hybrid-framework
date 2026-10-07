from decimal import Decimal
from enum import StrEnum
from typing import Self

import allure
from playwright.sync_api import Locator, Page

from saucedemo.models import Product
from saucedemo.pages.base_page import BasePage
from saucedemo.pages.components import Header
from saucedemo.utils.money import parse_price


class SortOption(StrEnum):
    NAME_ASC = "az"
    NAME_DESC = "za"
    PRICE_ASC = "lohi"
    PRICE_DESC = "hilo"


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = Header(page)
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.sort_select = page.get_by_test_id("product-sort-container")

    @property
    def loaded_marker(self) -> Locator:
        return self.items.first

    def _item_card(self, name: str) -> Locator:
        return self.items.filter(has=self.page.get_by_text(name, exact=True))

    def add_to_cart(self, *names: str) -> Self:
        for name in names:
            button = self._item_card(name).get_by_role("button", name="Add to cart")
            self.click(button, f"Add to cart: {name}")
        return self

    def get_product(self, name: str) -> Product:
        price_text = self.get_text(self._item_card(name).get_by_test_id("inventory-item-price"))
        return Product(name=name, price=parse_price(price_text))

    def get_product_names(self) -> list[str]:
        return [name.strip() for name in self.item_names.all_inner_texts()]

    def get_product_prices(self) -> list[Decimal]:
        return [parse_price(text) for text in self.item_prices.all_inner_texts()]

    def sort_by(self, option: SortOption) -> Self:
        with allure.step(f"Sort products by '{option.name}'"):
            self.sort_select.select_option(option.value)
        return self
