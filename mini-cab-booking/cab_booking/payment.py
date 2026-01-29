from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Mapping

from .models import PaymentReceipt, PaymentStatus, new_id


class PaymentMethodType(str, Enum):
    UPI = "UPI"
    CARD = "CARD"
    WALLET = "WALLET"


class PaymentMethod(ABC):
    """
    Payment abstraction: booking flow doesn't depend on concrete payment logic.
    """

    @abstractmethod
    def pay(self, amount: Decimal) -> PaymentReceipt:
        raise NotImplementedError

    @property
    @abstractmethod
    def method_name(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class UpiPayment(PaymentMethod):
    upi_id: str

    @property
    def method_name(self) -> str:
        return PaymentMethodType.UPI.value

    def pay(self, amount: Decimal) -> PaymentReceipt:
        if "@" not in self.upi_id:
            return PaymentReceipt(
                receipt_id=new_id("rcpt"),
                amount=amount,
                status=PaymentStatus.FAILED,
                method=self.method_name,
            )
        return PaymentReceipt(
            receipt_id=new_id("rcpt"),
            amount=amount,
            status=PaymentStatus.SUCCESS,
            method=self.method_name,
        )


@dataclass(frozen=True, slots=True)
class CardPayment(PaymentMethod):
    card_last4: str

    @property
    def method_name(self) -> str:
        return PaymentMethodType.CARD.value

    def pay(self, amount: Decimal) -> PaymentReceipt:
        if len(self.card_last4) != 4 or not self.card_last4.isdigit():
            return PaymentReceipt(
                receipt_id=new_id("rcpt"),
                amount=amount,
                status=PaymentStatus.FAILED,
                method=self.method_name,
            )
        return PaymentReceipt(
            receipt_id=new_id("rcpt"),
            amount=amount,
            status=PaymentStatus.SUCCESS,
            method=self.method_name,
        )


@dataclass(frozen=True, slots=True)
class WalletPayment(PaymentMethod):
    wallet_id: str
    balance: Decimal

    @property
    def method_name(self) -> str:
        return PaymentMethodType.WALLET.value

    def pay(self, amount: Decimal) -> PaymentReceipt:
        if self.balance < amount:
            return PaymentReceipt(
                receipt_id=new_id("rcpt"),
                amount=amount,
                status=PaymentStatus.FAILED,
                method=self.method_name,
            )
        return PaymentReceipt(
            receipt_id=new_id("rcpt"),
            amount=amount,
            status=PaymentStatus.SUCCESS,
            method=self.method_name,
        )


class PaymentFactory(ABC):
    """
    Abstract Factory: produces PaymentMethod objects.
    """

    @abstractmethod
    def create_upi(self, details: Mapping[str, Any]) -> PaymentMethod:
        raise NotImplementedError

    @abstractmethod
    def create_card(self, details: Mapping[str, Any]) -> PaymentMethod:
        raise NotImplementedError

    @abstractmethod
    def create_wallet(self, details: Mapping[str, Any]) -> PaymentMethod:
        raise NotImplementedError

    def create(self, payment_type: str, details: Mapping[str, Any]) -> PaymentMethod:
        """
        Factory Method: selects which concrete product to create.
        """
        normalized = payment_type.strip().upper()
        if normalized == PaymentMethodType.UPI.value:
            return self.create_upi(details)
        if normalized == PaymentMethodType.CARD.value:
            return self.create_card(details)
        if normalized == PaymentMethodType.WALLET.value:
            return self.create_wallet(details)
        raise ValueError(f"Unsupported payment type: {payment_type!r}")


class DefaultPaymentFactory(PaymentFactory):
    def create_upi(self, details: Mapping[str, Any]) -> PaymentMethod:
        return UpiPayment(upi_id=str(details.get("upi_id", "")))

    def create_card(self, details: Mapping[str, Any]) -> PaymentMethod:
        # Never store raw card numbers; keep only last4 for demo.
        last4 = str(details.get("card_last4", ""))
        return CardPayment(card_last4=last4)

    def create_wallet(self, details: Mapping[str, Any]) -> PaymentMethod:
        wallet_id = str(details.get("wallet_id", ""))
        balance = Decimal(str(details.get("balance", "0")))
        return WalletPayment(wallet_id=wallet_id, balance=balance)

