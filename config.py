"""Project-wide configuration for MVP calculators."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Static settings used across calculators and UI."""

    app_title: str = "Commercial Calculators MVP"
    default_presence_beta: float = 1.2
    default_presence_cap_uplift: float = 0.5
    default_overlap_coeff: float = 0.85
    default_promo_share_of_period: float = 1.0


settings = Settings()
