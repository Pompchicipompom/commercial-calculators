"""Pydantic schemas for promo ROI modeling."""

from pydantic import BaseModel, Field


class PromoInput(BaseModel):
    """Input payload for promo ROI calculations."""

    baseline_units: float = Field(gt=0, description="Expected baseline units without promo.")
    promo_units: float = Field(gt=0, description="Expected units during promo period.")
    promo_price: float = Field(gt=0, description="Average realized promo price per unit.")
    unit_variable_cost: float = Field(gt=0, description="Variable cost per unit.")
    promo_cost_fixed: float = Field(
        ge=0, description="Fixed promo investment (listing, display, fees)."
    )
    promo_cost_variable: float = Field(
        ge=0, description="Variable promo investment (rebates, variable mechanics)."
    )


class PromoResult(BaseModel):
    """Result of promo ROI calculations."""

    incremental_units: float
    incremental_margin: float
    promo_total_cost: float
    net_effect: float
    roi: float
    break_even_incremental_units: float
