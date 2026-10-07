"""Restful-Booker client on Playwright's APIRequestContext.

Methods return the raw ``APIResponse`` so tests can assert on status codes for
negative scenarios; parsing into models is the caller's decision.
"""

from typing import Any

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from saucedemo.models import Booking


class AuthenticationError(Exception):
    pass


class BookingClient:
    def __init__(self, request: APIRequestContext) -> None:
        self._request = request

    # ---------- auth ----------

    def auth(self, username: str, password: str) -> APIResponse:
        return self._send("POST", "/auth", data={"username": username, "password": password})

    def create_token(self, username: str, password: str) -> str:
        # Restful-Booker answers 200 {"reason": "Bad credentials"} on failure, so check the body
        token = self.auth(username, password).json().get("token")
        if not token:
            raise AuthenticationError(f"No token issued for user {username!r}")
        return token

    # ---------- bookings ----------

    def create_booking(self, booking: Booking) -> APIResponse:
        return self._send("POST", "/booking", data=booking.model_dump(mode="json"))

    def get_booking(self, booking_id: int) -> APIResponse:
        return self._send("GET", f"/booking/{booking_id}")

    def update_booking(
        self, booking_id: int, booking: Booking, token: str | None = None
    ) -> APIResponse:
        return self._send(
            "PUT", f"/booking/{booking_id}", token=token, data=booking.model_dump(mode="json")
        )

    def delete_booking(self, booking_id: int, token: str | None = None) -> APIResponse:
        return self._send("DELETE", f"/booking/{booking_id}", token=token)

    # ---------- transport ----------

    def _send(
        self, method: str, url: str, *, token: str | None = None, **kwargs: Any
    ) -> APIResponse:
        headers = {"Cookie": f"token={token}"} if token else {}
        with allure.step(f"{method} {url}"):
            response = self._request.fetch(url, method=method, headers=headers, **kwargs)
            allure.attach(
                f"{response.status} {response.status_text}\n\n{response.text()}",
                name=f"{method} {url} -> {response.status}",
                attachment_type=allure.attachment_type.TEXT,
            )
        return response
