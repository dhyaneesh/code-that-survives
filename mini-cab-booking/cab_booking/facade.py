from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import replace

from .config import AppConfig
from .models import Booking, BookingStatus, PaymentStatus, RideRequest
from .observer import Event, EventBus
from .payment import PaymentFactory
from .pricing import PricingStrategy
from .services import AuthService, BookingService


class RideBookingFacade(ABC):
    """
    Facade interface (used by wrappers so we can add cross-cutting concerns).
    """

    @abstractmethod
    def book_ride(self, request: RideRequest) -> Booking:
        raise NotImplementedError

    @abstractmethod
    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        raise NotImplementedError


class CabBookingFacade(RideBookingFacade):
    """
    Facade pattern:
    - One entrypoint to orchestrate pricing + booking + payment + events
    - Keeps low coupling via abstractions (strategies + factories)
    """

    def __init__(
        self,
        *,
        config: AppConfig,
        pricing_strategy: PricingStrategy,
        payment_factory: PaymentFactory,
        booking_service: BookingService,
        event_bus: EventBus | None = None,
    ) -> None:
        self._config = config
        self._pricing_strategy = pricing_strategy
        self._payment_factory = payment_factory
        self._booking_service = booking_service
        self._event_bus = event_bus or EventBus()

    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        self._pricing_strategy = strategy
        self._event_bus.publish(
            Event(
                event_type="PRICING_STRATEGY_CHANGED",
                payload={"strategy": type(strategy).__name__},
            )
        )

    def book_ride(self, request: RideRequest) -> Booking:
        # NOTE: No authentication/logging here by design.
        # Those concerns are added by wrappers WITHOUT changing this method.

        fare = self._pricing_strategy.calculate_fare(request.distance_km)
        self._event_bus.publish(
            Event(
                event_type="FARE_CALCULATED",
                payload={"distance_km": request.distance_km, "fare": str(fare)},
            )
        )

        booking = self._booking_service.create_booking(request=request, fare=fare)
        self._event_bus.publish(
            Event(
                event_type="DRIVER_ASSIGNED",
                payload={
                    "booking_id": booking.booking_id,
                    "driver_id": booking.driver.driver_id if booking.driver else None,
                },
            )
        )

        payment_method = self._payment_factory.create(
            request.payment_type, request.payment_details
        )
        receipt = payment_method.pay(fare)

        self._event_bus.publish(
            Event(
                event_type="PAYMENT_PROCESSED",
                payload={
                    "booking_id": booking.booking_id,
                    "method": receipt.method,
                    "status": receipt.status.value,
                },
            )
        )

        if receipt.status == PaymentStatus.SUCCESS:
            booking = replace(
                booking, payment=receipt, status=BookingStatus.CONFIRMED
            )
            self._event_bus.publish(
                Event(
                    event_type="BOOKING_CONFIRMED",
                    payload={
                        "booking_id": booking.booking_id,
                        "fare": f"{self._config.currency_symbol}{fare}",
                        "app": self._config.app_name,
                    },
                )
            )
            return booking

        booking = replace(booking, payment=receipt, status=BookingStatus.FAILED)
        self._event_bus.publish(
            Event(
                event_type="BOOKING_FAILED",
                payload={"booking_id": booking.booking_id, "reason": "payment_failed"},
            )
        )
        return booking

    @property
    def event_bus(self) -> EventBus:
        return self._event_bus


class LoggedFacade(RideBookingFacade):
    """
    Proxy/Decorator-style wrapper: adds logging without modifying core book_ride().
    """

    def __init__(self, inner: RideBookingFacade, logger: logging.Logger | None = None):
        self._inner = inner
        self._logger = logger or logging.getLogger("mini_cab_booking")

    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        self._logger.info("pricing_strategy_change strategy=%s", type(strategy).__name__)
        self._inner.set_pricing_strategy(strategy)

    def book_ride(self, request: RideRequest) -> Booking:
        self._logger.info(
            "book_ride start rider=%s distance_km=%s payment=%s",
            request.rider.rider_id,
            request.distance_km,
            request.payment_type,
        )
        booking = self._inner.book_ride(request)
        self._logger.info(
            "book_ride end booking_id=%s status=%s",
            booking.booking_id,
            booking.status.value,
        )
        return booking


class AuthenticatedFacade(RideBookingFacade):
    """
    Proxy/Decorator-style wrapper: adds authentication without modifying core book_ride().
    """

    def __init__(self, inner: RideBookingFacade, auth_service: AuthService):
        self._inner = inner
        self._auth = auth_service

    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        self._inner.set_pricing_strategy(strategy)

    def book_ride(self, request: RideRequest) -> Booking:
        if not self._auth.is_authenticated(request.auth_token):
            raise PermissionError("Access denied: invalid or missing auth token")
        return self._inner.book_ride(request)

