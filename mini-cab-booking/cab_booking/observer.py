from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, DefaultDict


@dataclass(frozen=True, slots=True)
class Event:
    event_type: str
    payload: dict[str, Any]


class Observer(ABC):
    @abstractmethod
    def on_event(self, event: Event) -> None:
        raise NotImplementedError


class EventBus:
    """
    Observer pattern: decouple booking/payment flow from notifications/logging.
    """

    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, list[Observer]] = DefaultDict(list)

    def subscribe(self, event_type: str, observer: Observer) -> None:
        self._subscribers[event_type].append(observer)

    def publish(self, event: Event) -> None:
        for observer in list(self._subscribers.get(event.event_type, [])):
            observer.on_event(event)


class ConsoleObserver(Observer):
    def __init__(self, prefix: str = "EVENT") -> None:
        self._prefix = prefix

    def on_event(self, event: Event) -> None:
        print(f"[{self._prefix}] {event.event_type}: {event.payload}")

