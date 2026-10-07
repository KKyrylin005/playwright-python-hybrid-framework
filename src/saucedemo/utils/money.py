import re
from decimal import Decimal

_PRICE_PATTERN = re.compile(r"\$(\d+(?:\.\d{2})?)")


def parse_price(text: str) -> Decimal:
    """Extract a dollar amount from UI text, e.g. 'Item total: $39.98' -> Decimal('39.98')."""
    match = _PRICE_PATTERN.search(text)
    if match is None:
        raise ValueError(f"No price found in text: {text!r}")
    return Decimal(match.group(1))
