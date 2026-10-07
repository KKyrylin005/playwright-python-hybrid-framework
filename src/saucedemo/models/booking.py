"""Restful-Booker API contracts.

Pydantic (not dataclasses) because these models double as JSON schema checks:
``extra="forbid"`` makes any unexpected field in a response fail validation.
"""

from datetime import date

from pydantic import BaseModel, ConfigDict


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class BookingDates(_StrictModel):
    checkin: date
    checkout: date


class Booking(_StrictModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str | None = None


class CreatedBooking(_StrictModel):
    bookingid: int
    booking: Booking
