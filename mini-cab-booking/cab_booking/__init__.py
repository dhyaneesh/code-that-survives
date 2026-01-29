"""
Mini Cab Booking System (Uber/Ola-like) — OOP + patterns demo.

Patterns used:
- Singleton (AppConfig)
- Strategy (PricingStrategy)
- Abstract Factory / Factory Method (PaymentFactory)
- Builder (RideRequestBuilder)
- Observer (EventBus + observers)
- Facade (CabBookingFacade)
- Proxy/Decorator style wrappers (LoggedFacade / AuthenticatedFacade)
"""

from .config import AppConfig
from .builder import RideRequestBuilder
from .facade import (
    AuthenticatedFacade,
    CabBookingFacade,
    LoggedFacade,
)
from .observer import EventBus
from .payment import DefaultPaymentFactory, PaymentMethodType
from .pricing import NormalPricing, SurgePricing

__all__ = [
    "AppConfig",
    "AuthenticatedFacade",
    "CabBookingFacade",
    "DefaultPaymentFactory",
    "EventBus",
    "LoggedFacade",
    "NormalPricing",
    "PaymentMethodType",
    "RideRequestBuilder",
    "SurgePricing",
]

