from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class OrderSummary:
    """Price block shown on the checkout overview page."""

    subtotal: Decimal
    tax: Decimal
    total: Decimal
