from decimal import Decimal

import allure
import pytest

from saucedemo.utils.money import parse_price

pytestmark = [pytest.mark.unit, allure.epic("Framework"), allure.feature("Utils: money")]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("$29.99", Decimal("29.99"), id="bare-price"),
        pytest.param("Item total: $39.98", Decimal("39.98"), id="labelled-price"),
        pytest.param("Tax: $3.20", Decimal("3.20"), id="keeps-trailing-zero"),
        pytest.param("$7", Decimal("7"), id="no-cents"),
    ],
)
def test_parse_price_extracts_amount(text: str, expected: Decimal) -> None:
    assert parse_price(text) == expected


def test_parse_price_returns_decimal_not_float() -> None:
    assert isinstance(parse_price("$0.10"), Decimal)


def test_parse_price_rejects_text_without_amount() -> None:
    with pytest.raises(ValueError, match="No price found"):
        parse_price("Free shipping")
