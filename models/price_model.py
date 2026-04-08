"""Pydantic schemas for price impact modeling."""

from pydantic import BaseModel, Field


class PriceInput(BaseModel):
    """Input payload for price impact calculations."""

    baseline_units: float = Field(gt=0, description="Baseline units at old price.")
    old_price: float = Field(gt=0, description="Current average selling price.")
    new_price: float = Field(gt=0, description="Planned average selling price.")
    elasticity: float = Field(
        lt=0,
        description="Price elasticity coefficient (negative for standard demand curves).",
    )
    unit_variable_cost: float = Field(gt=0, description="Variable cost per unit.")


class PriceImpactResult(BaseModel):
    """Result of price impact calculations."""

    volume_factor: float = Field(gt=0)
    new_units: float
    new_revenue: float
    new_margin: float
    incremental_margin: float
