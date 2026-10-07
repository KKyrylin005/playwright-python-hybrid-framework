import allure
import pytest

from saucedemo.pages import InventoryPage, SortOption

pytestmark = [pytest.mark.ui, allure.epic("SauceDemo"), allure.feature("Inventory")]


@pytest.mark.regression
@allure.title("Products are sorted by price: {option.name}")
@pytest.mark.parametrize(
    ("option", "descending"),
    [(SortOption.PRICE_ASC, False), (SortOption.PRICE_DESC, True)],
    ids=["price-low-to-high", "price-high-to-low"],
)
def test_sort_by_price(inventory_page: InventoryPage, option: SortOption, descending: bool) -> None:
    prices = inventory_page.sort_by(option).get_product_prices()

    assert prices == sorted(prices, reverse=descending)


@pytest.mark.regression
@allure.title("Products are sorted by name: {option.name}")
@pytest.mark.parametrize(
    ("option", "descending"),
    [(SortOption.NAME_ASC, False), (SortOption.NAME_DESC, True)],
    ids=["name-a-to-z", "name-z-to-a"],
)
def test_sort_by_name(inventory_page: InventoryPage, option: SortOption, descending: bool) -> None:
    names = inventory_page.sort_by(option).get_product_names()

    assert names == sorted(names, reverse=descending)
