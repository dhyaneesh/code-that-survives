from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Location:
    lat: float
    lng: float


@dataclass(frozen=True, slots=True)
class Rider:
    rider_id: str
    name: str


@dataclass(frozen=True, slots=True)
class Driver:
    driver_id: str
    name: str


class BookingStatus(str, Enum):
    CREATED = "CREATED"
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"


class PaymentStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


@dataclass(frozen=True, slots=True)
class RideRequest:
    rider: Rider
    pickup: Location
    drop: Location
    distance_km: float
    payment_type: str
    payment_details: dict[str, Any]
    auth_token: str | None = None


@dataclass(frozen=True, slots=True)
class PaymentReceipt:
    receipt_id: str
    amount: Decimal
    status: PaymentStatus
    method: str


@dataclass(frozen=True, slots=True)
class Booking:
    booking_id: str
    request: RideRequest
    fare: Decimal
    status: BookingStatus
    driver: Driver | None = None
    payment: PaymentReceipt | None = None


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"

