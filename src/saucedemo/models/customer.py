from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Customer:
    """Shipping information entered on the checkout step one."""

    first_name: str
    last_name: str
    postal_code: str
