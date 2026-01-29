from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import Location, RideRequest, Rider


@dataclass(slots=True)
class RideRequestBuilder:
    """
    Builder pattern: construct a validated RideRequest via a fluent API.
    """

    _rider: Rider | None = None
    _pickup: Location | None = None
    _drop: Location | None = None
    _distance_km: float | None = None
    _payment_type: str | None = None
    _payment_details: dict[str, Any] | None = None
    _auth_token: str | None = None

    def rider(self, rider_id: str, name: str) -> "RideRequestBuilder":
        self._rider = Rider(rider_id=rider_id, name=name)
        return self

    def pickup(self, lat: float, lng: float) -> "RideRequestBuilder":
        self._pickup = Location(lat=lat, lng=lng)
        return self

    def drop(self, lat: float, lng: float) -> "RideRequestBuilder":
        self._drop = Location(lat=lat, lng=lng)
        return self

    def distance_km(self, km: float) -> "RideRequestBuilder":
        self._distance_km = km
        return self

    def payment(self, payment_type: str, **details: Any) -> "RideRequestBuilder":
        self._payment_type = payment_type
        self._payment_details = dict(details)
        return self

    def auth_token(self, token: str | None) -> "RideRequestBuilder":
        self._auth_token = token
        return self

    def build(self) -> RideRequest:
        missing: list[str] = []
        if self._rider is None:
            missing.append("rider")
        if self._pickup is None:
            missing.append("pickup")
        if self._drop is None:
            missing.append("drop")
        if self._distance_km is None:
            missing.append("distance_km")
        if self._payment_type is None:
            missing.append("payment_type")
        if self._payment_details is None:
            missing.append("payment_details")

        if missing:
            raise ValueError(f"RideRequestBuilder missing fields: {', '.join(missing)}")

        return RideRequest(
            rider=self._rider,
            pickup=self._pickup,
            drop=self._drop,
            distance_km=float(self._distance_km),
            payment_type=str(self._payment_type),
            payment_details=dict(self._payment_details),
            auth_token=self._auth_token,
        )

