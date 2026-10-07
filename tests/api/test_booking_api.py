import allure
import pytest

from saucedemo.api import BookingClient
from saucedemo.data import make_booking
from saucedemo.models import Booking, CreatedBooking

pytestmark = [pytest.mark.api, allure.epic("Restful-Booker"), allure.feature("Booking API")]


@pytest.mark.smoke
@allure.title("Created booking is returned with a valid schema and the sent data")
def test_create_booking(booking_client: BookingClient, auth_token: str) -> None:
    payload = make_booking()

    response = booking_client.create_booking(payload)

    assert response.status == 200
    created = CreatedBooking.model_validate(response.json())  # schema check
    try:
        assert created.booking == payload
    finally:
        booking_client.delete_booking(created.bookingid, token=auth_token)


@pytest.mark.regression
@allure.title("Booking can be read back by id")
def test_get_booking_by_id(booking_client: BookingClient, created_booking: CreatedBooking) -> None:
    response = booking_client.get_booking(created_booking.bookingid)

    assert response.status == 200
    assert Booking.model_validate(response.json()) == created_booking.booking


@pytest.mark.regression
@allure.title("Authorised user can update a booking")
def test_update_booking_with_token(
    booking_client: BookingClient, created_booking: CreatedBooking, auth_token: str
) -> None:
    updated = created_booking.booking.model_copy(update={"firstname": "Updated", "totalprice": 999})

    response = booking_client.update_booking(created_booking.bookingid, updated, token=auth_token)

    assert response.status == 200
    stored = Booking.model_validate(booking_client.get_booking(created_booking.bookingid).json())
    assert stored == updated


@pytest.mark.regression
@allure.title("Update without a token is forbidden and leaves the booking unchanged")
def test_update_booking_without_token_is_forbidden(
    booking_client: BookingClient, created_booking: CreatedBooking
) -> None:
    updated = created_booking.booking.model_copy(update={"firstname": "Hacker"})

    response = booking_client.update_booking(created_booking.bookingid, updated)

    assert response.status == 403
    stored = Booking.model_validate(booking_client.get_booking(created_booking.bookingid).json())
    assert stored == created_booking.booking


@pytest.mark.regression
@allure.title("Deleted booking is no longer available")
def test_delete_booking(
    booking_client: BookingClient, created_booking: CreatedBooking, auth_token: str
) -> None:
    response = booking_client.delete_booking(created_booking.bookingid, token=auth_token)

    assert response.status == 201  # Restful-Booker's documented (non-standard) status
    assert booking_client.get_booking(created_booking.bookingid).status == 404


@pytest.mark.regression
@allure.title("Auth with bad credentials issues no token")
def test_auth_with_bad_credentials(booking_client: BookingClient) -> None:
    response = booking_client.auth("admin", "wrong-password")

    assert response.status == 200  # the API reports the error in the body, not the status
    assert response.json() == {"reason": "Bad credentials"}
