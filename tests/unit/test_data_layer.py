from decimal import Decimal

import allure
import pytest

from saucedemo.data import get_product, load_products, load_users, make_booking, make_customer

pytestmark = [pytest.mark.unit, allure.epic("Framework"), allure.feature("Test data")]


def test_catalog_ids_and_names_are_unique() -> None:
    products = load_products()

    assert len({product.id for product in products}) == len(products)
    assert len({product.name for product in products}) == len(products)


def test_catalog_prices_are_positive_decimals() -> None:
    for product in load_products():
        assert isinstance(product.price, Decimal)
        assert product.price > 0


def test_get_product_by_name() -> None:
    assert get_product("Sauce Labs Backpack").id == 4


def test_get_product_unknown_name_fails_with_clear_message() -> None:
    with pytest.raises(KeyError, match="Unknown product: 'Sauce Labs Spaceship'"):
        get_product("Sauce Labs Spaceship")


def test_users_share_the_configured_password() -> None:
    users = load_users("pa55")

    assert "standard" in users
    assert {user.password for user in users.values()} == {"pa55"}


def test_user_password_is_hidden_from_repr() -> None:
    user = load_users("pa55")["standard"]

    assert "pa55" not in repr(user)


def test_factories_generate_unique_data() -> None:
    assert make_customer() != make_customer()
    assert make_booking().firstname != make_booking().firstname


def test_booking_dates_are_ordered() -> None:
    dates = make_booking().bookingdates

    assert dates.checkout > dates.checkin


def test_booking_factory_accepts_overrides() -> None:
    assert make_booking(firstname="Override").firstname == "Override"
