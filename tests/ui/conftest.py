import pytest

from saucedemo.models import Customer, User
from saucedemo.pages import InventoryPage, LoginPage


@pytest.fixture
def inventory_page(login_page: LoginPage, standard_user: User) -> InventoryPage:
    """Authorised start point. Step 7 swaps the UI login for session injection."""
    return login_page.login(standard_user)


@pytest.fixture
def customer() -> Customer:
    return Customer(first_name="John", last_name="Doe", postal_code="10001")
