"""Project-wide configuration for MVP calculators."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Static settings used across calculators and UI."""

    app_title: str = (
        "\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 "
        "\u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u0430 "
        "\u0440\u043e\u0441\u0442\u0430 \u043f\u0440\u043e\u0434\u0430\u0436"
    )
    default_presence_beta: float = 1.2
    default_presence_cap_uplift: float = 0.5
    default_overlap_coeff: float = 0.85
    default_promo_share_of_period: float = 1.0


settings = Settings()
