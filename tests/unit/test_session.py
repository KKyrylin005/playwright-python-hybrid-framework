import json

import allure
import pytest

from saucedemo.utils.session import CART_STORAGE_KEY, SESSION_COOKIE, build_storage_state

pytestmark = [pytest.mark.unit, allure.epic("Framework"), allure.feature("Utils: session")]

BASE_URL = "https://www.saucedemo.com"


def test_session_cookie_targets_base_url_host() -> None:
    state = build_storage_state(BASE_URL, "standard_user")

    [cookie] = state["cookies"]
    assert cookie["name"] == SESSION_COOKIE
    assert cookie["value"] == "standard_user"
    assert cookie["domain"] == "www.saucedemo.com"
    assert cookie["path"] == "/"


def test_cart_is_stored_as_json_list_of_ids() -> None:
    state = build_storage_state(BASE_URL, "standard_user", cart_product_ids=[4, 0])

    [origin] = state["origins"]
    assert origin["origin"] == BASE_URL
    [entry] = origin["localStorage"]
    assert entry["name"] == CART_STORAGE_KEY
    assert json.loads(entry["value"]) == [4, 0]


def test_empty_cart_writes_no_local_storage() -> None:
    state = build_storage_state(BASE_URL, "standard_user")

    [origin] = state["origins"]
    assert origin["localStorage"] == []


def test_cart_accepts_any_iterable() -> None:
    state = build_storage_state(BASE_URL, "standard_user", cart_product_ids=iter((1, 2)))

    [entry] = state["origins"][0]["localStorage"]
    assert json.loads(entry["value"]) == [1, 2]
