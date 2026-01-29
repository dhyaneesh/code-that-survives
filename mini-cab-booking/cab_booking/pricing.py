from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP


class PricingStrategy(ABC):
    """
    Strategy pattern: pricing is interchangeable at runtime.
    """

    @abstractmethod
    def calculate_fare(self, distance_km: float) -> Decimal:
        raise NotImplementedError


class PerKmPricing(PricingStrategy):
    def __init__(self, rate_per_km: Decimal):
        self._rate_per_km = rate_per_km

    def calculate_fare(self, distance_km: float) -> Decimal:
        if distance_km <= 0:
            raise ValueError("distance_km must be > 0")
        amount = (Decimal(str(distance_km)) * self._rate_per_km).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return amount

    @property
    def rate_per_km(self) -> Decimal:
        return self._rate_per_km


class NormalPricing(PerKmPricing):
    """
    Normal pricing: ₹10/km
    """

    def __init__(self):
        super().__init__(rate_per_km=Decimal("10"))


class SurgePricing(PerKmPricing):
    """
    Surge pricing: ₹25/km
    """

    def __init__(self):
        super().__init__(rate_per_km=Decimal("25"))

