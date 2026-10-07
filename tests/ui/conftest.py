import pytest

from saucedemo.models import User
from saucedemo.pages import InventoryPage, LoginPage


@pytest.fixture
def inventory_page(login_page: LoginPage, standard_user: User) -> InventoryPage:
    """Pure-UI start point: logs in through the form (see tests/hybrid for the fast path)."""
    return login_page.login(standard_user)
