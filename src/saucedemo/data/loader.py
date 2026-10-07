"""Static test data shipped with the package, importable at collection time (parametrize)."""

import json
from decimal import Decimal
from functools import cache
from importlib.resources import files
from typing import Any

from saucedemo.models import Product, User


def _read_json(name: str) -> Any:
    return json.loads(files(__package__).joinpath(name).read_text(encoding="utf-8"))


@cache
def load_products() -> tuple[Product, ...]:
    return tuple(
        Product(id=item["id"], name=item["name"], price=Decimal(item["price"]))
        for item in _read_json("products.json")
    )


def get_product(name: str) -> Product:
    for product in load_products():
        if product.name == name:
            return product
    raise KeyError(f"Unknown product: {name!r}")  # e.g. a typo in @pytest.mark.cart


def load_users(password: str) -> dict[str, User]:
    """Users by role; SauceDemo shares one password, so it comes from settings."""
    return {
        role: User(username=data["username"], password=password)
        for role, data in _read_json("users.json").items()
    }
