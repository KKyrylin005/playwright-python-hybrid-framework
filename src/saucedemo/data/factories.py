"""Dynamic test data: unique values per call so parallel tests never collide."""

import random
import string
from datetime import date, timedelta

from saucedemo.models import Booking, BookingDates, Customer


def _suffix(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def make_customer() -> Customer:
    return Customer(
        first_name=f"John-{_suffix()}",
        last_name=f"Doe-{_suffix()}",
        postal_code=f"{random.randint(10000, 99999)}",
    )


def make_booking(**overrides: object) -> Booking:
    checkin = date.today() + timedelta(days=random.randint(1, 30))
    defaults = {
        "firstname": f"Jane-{_suffix()}",
        "lastname": f"Tester-{_suffix()}",
        "totalprice": random.randint(50, 500),
        "depositpaid": random.choice([True, False]),
        "bookingdates": BookingDates(
            checkin=checkin, checkout=checkin + timedelta(days=random.randint(1, 7))
        ),
        "additionalneeds": "Breakfast",
    }
    return Booking.model_validate({**defaults, **overrides})
