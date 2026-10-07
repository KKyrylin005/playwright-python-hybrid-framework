import re

import allure
import pytest
from playwright.sync_api import expect

from saucedemo.config import get_settings
from saucedemo.models import User
from saucedemo.pages import InventoryPage, LoginPage

PASSWORD = get_settings().password.get_secret_value()

pytestmark = [pytest.mark.ui, allure.epic("SauceDemo"), allure.feature("Authentication")]


@pytest.mark.smoke
@allure.title("Standard user logs in and lands on the inventory page")
def test_standard_user_can_log_in(login_page: LoginPage, standard_user: User) -> None:
    inventory = login_page.login(standard_user)

    expect(inventory.page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory.title).to_have_text("Products")


@pytest.mark.regression
@allure.title("Login is rejected with error: '{expected_error}'")
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param(
            "locked_out_user", PASSWORD, "this user has been locked out", id="locked-out-user"
        ),
        pytest.param(
            "standard_user", "wrong_password", "do not match any user", id="wrong-password"
        ),
        pytest.param("", PASSWORD, "Username is required", id="empty-username"),
        pytest.param("standard_user", "", "Password is required", id="empty-password"),
    ],
)
def test_login_rejected_with_error(
    login_page: LoginPage, username: str, password: str, expected_error: str
) -> None:
    login_page.submit_credentials(username, password)

    expect(login_page.error_message).to_contain_text(expected_error)
    expect(login_page.login_button).to_be_visible()


@pytest.mark.regression
@allure.title("Logged-in user can log out")
def test_user_can_log_out(inventory_page: InventoryPage) -> None:
    login_page = inventory_page.header.logout()

    expect(login_page.username_input).to_be_empty()
    expect(login_page.page).not_to_have_url(re.compile(r"/inventory\.html$"))
