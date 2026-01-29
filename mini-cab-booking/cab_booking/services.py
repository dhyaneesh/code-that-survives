from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from .models import Booking, BookingStatus, Driver, RideRequest, new_id


class AuthService:
    """
    Simple authentication service used by a proxy wrapper.
    """

    def __init__(self, valid_tokens: Iterable[str] | None = None) -> None:
        self._valid = set(valid_tokens or [])

    def is_authenticated(self, token: str | None) -> bool:
        if token is None:
            return False
        if token in self._valid:
            return True
        # Demo fallback: accept tokens that follow a pattern.
        return token.startswith("token-")


class DriverAllocator:
    """
    Very small driver assignment component (can be replaced later).
    """

    def __init__(self, drivers: list[Driver]) -> None:
        if not drivers:
            raise ValueError("drivers list must not be empty")
        self._drivers = drivers
        self._idx = 0

    def allocate(self, _request: RideRequest) -> Driver:
        driver = self._drivers[self._idx % len(self._drivers)]
        self._idx += 1
        return driver


class BookingService:
    """
    Core booking creation/driver assignment.
    Intentionally does not include auth/logging to keep concerns separated.
    """

    def __init__(self, allocator: DriverAllocator) -> None:
        self._allocator = allocator

    def create_booking(self, request: RideRequest, fare) -> Booking:
        booking = Booking(
            booking_id=new_id("bk"),
            request=request,
            fare=fare,
            status=BookingStatus.CREATED,
            driver=None,
            payment=None,
        )
        driver = self._allocator.allocate(request)
        booking = replace(booking, driver=driver, status=BookingStatus.DRIVER_ASSIGNED)
        booking = replace(booking, status=BookingStatus.PAYMENT_PENDING)
        return booking

