from __future__ import annotations


class AppConfig:
    """
    Singleton shared configuration.

    Requirement:
    - Maintain a single, shared application configuration containing:
      - app name
      - currency symbol
    """

    _instance: "AppConfig | None" = None

    def __new__(cls, app_name: str = "MiniCab", currency_symbol: str = "₹"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.app_name = app_name
            cls._instance.currency_symbol = currency_symbol
        return cls._instance

    def __repr__(self) -> str:
        return f"AppConfig(app_name={self.app_name!r}, currency_symbol={self.currency_symbol!r})"

