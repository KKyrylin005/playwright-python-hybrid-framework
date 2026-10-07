from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from saucedemo.api import BookingClient
from saucedemo.config import Settings
from saucedemo.data import make_booking
from saucedemo.models import CreatedBooking


@pytest.fixture(scope="session")
def api_request_context(
    playwright_instance: Playwright, settings: Settings
) -> Generator[APIRequestContext, None, None]:
    """No browser is launched for API tests: only Playwright's HTTP client."""
    context = playwright_instance.request.new_context(
        base_url=settings.booker_base_url,
        extra_http_headers={"Accept": "application/json"},
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def booking_client(api_request_context: APIRequestContext) -> BookingClient:
    return BookingClient(api_request_context)


@pytest.fixture(scope="session")
def auth_token(booking_client: BookingClient, settings: Settings) -> str:
    return booking_client.create_token(
        settings.booker_username, settings.booker_password.get_secret_value()
    )


@pytest.fixture
def created_booking(
    booking_client: BookingClient, auth_token: str
) -> Generator[CreatedBooking, None, None]:
    """Booking created via API before the test and removed after it (even if already deleted)."""
    response = booking_client.create_booking(make_booking())
    assert response.ok, f"Precondition failed: booking not created ({response.status})"
    created = CreatedBooking.model_validate(response.json())

    yield created

    booking_client.delete_booking(created.bookingid, token=auth_token)
