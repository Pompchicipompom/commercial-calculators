"""Unified scenario engine combining multiple commercial drivers."""

from typing import Optional

from pydantic import BaseModel, Field

from calculators.presence_calculator import calculate_presence_uplift
from calculators.price_impact_calculator import calculate_price_impact
from models.presence_model import PresenceInput
from models.price_model import PriceInput
from models.promo_model import PromoInput


class ScenarioInput(BaseModel):
    """Input for unified scenario simulation."""

    baseline_units: float = Field(gt=0)
    baseline_price: float = Field(gt=0)
    unit_variable_cost: float = Field(gt=0)
    promo_share_of_period: float = Field(default=1.0, ge=0, le=1)
    overlap_coeff: float = Field(default=0.85, ge=0, le=1)

    presence_input: Optional[PresenceInput] = None
    promo_input: Optional[PromoInput] = None
    price_input: Optional[PriceInput] = None


class ScenarioResult(BaseModel):
    """Output from unified scenario simulation."""

    adjusted_volume_factor: float
    scenario_units: float
    scenario_price: float
    scenario_revenue: float
    scenario_margin: float
    incremental_margin: float
    estimated_investment: float
    scenario_roi: float
    component_presence_uplift_pct: float
    component_promo_uplift_pct: float
    component_price_factor: float


def calculate_unified_scenario(payload: ScenarioInput) -> ScenarioResult:
    """
    Calculate a combined scenario across presence, promo and price drivers.

    Effects are combined multiplicatively and adjusted by overlap_coeff to avoid
    unrealistic double counting in an MVP setting.
    """

    presence_uplift_pct = 0.0
    if payload.presence_input is not None:
        presence_result = calculate_presence_uplift(payload.presence_input)
        presence_uplift_pct = presence_result.uplift_pct

    promo_uplift_pct = 0.0
    promo_investment = 0.0
    promo_price = None
    if payload.promo_input is not None:
        promo_baseline = payload.promo_input.baseline_units
        promo_uplift_pct = max(
            (payload.promo_input.promo_units - promo_baseline) / promo_baseline,
            0.0,
        )
        promo_investment = (
            payload.promo_input.promo_cost_fixed + payload.promo_input.promo_cost_variable
        )
        promo_price = payload.promo_input.promo_price

    price_factor = 1.0
    scenario_price = payload.baseline_price
    if payload.price_input is not None:
        price_result = calculate_price_impact(payload.price_input)
        price_factor = price_result.volume_factor
        scenario_price = payload.price_input.new_price

    raw_factor = (
        (1 + presence_uplift_pct)
        * (1 + promo_uplift_pct * payload.promo_share_of_period)
        * price_factor
    )
    adjusted_factor = 1 + (raw_factor - 1) * payload.overlap_coeff
    scenario_units = payload.baseline_units * adjusted_factor

    if promo_price is not None and payload.promo_share_of_period > 0:
        scenario_price = (
            scenario_price * (1 - payload.promo_share_of_period)
            + promo_price * payload.promo_share_of_period
        )

    baseline_margin = payload.baseline_units * (
        payload.baseline_price - payload.unit_variable_cost
    )
    scenario_revenue = scenario_units * scenario_price
    scenario_margin = scenario_units * (scenario_price - payload.unit_variable_cost)
    incremental_margin = scenario_margin - baseline_margin

    if promo_investment > 0:
        scenario_roi = (incremental_margin - promo_investment) / promo_investment
    else:
        scenario_roi = float("inf") if incremental_margin > 0 else 0.0

    return ScenarioResult(
        adjusted_volume_factor=adjusted_factor,
        scenario_units=scenario_units,
        scenario_price=scenario_price,
        scenario_revenue=scenario_revenue,
        scenario_margin=scenario_margin,
        incremental_margin=incremental_margin,
        estimated_investment=promo_investment,
        scenario_roi=scenario_roi,
        component_presence_uplift_pct=presence_uplift_pct,
        component_promo_uplift_pct=promo_uplift_pct,
        component_price_factor=price_factor,
    )
