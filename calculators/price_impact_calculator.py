"""Calculator for price elasticity impact on volume and margin."""

from models.price_model import PriceImpactResult, PriceInput


def calculate_price_impact(payload: PriceInput) -> PriceImpactResult:
    """
    Calculate price impact using a log-log elasticity assumption.

    Formula:
    volume_factor = (new_price / old_price) ** elasticity
    """

    volume_factor = (payload.new_price / payload.old_price) ** payload.elasticity
    new_units = payload.baseline_units * volume_factor
    new_revenue = new_units * payload.new_price

    new_margin = new_units * (payload.new_price - payload.unit_variable_cost)
    baseline_margin = payload.baseline_units * (
        payload.old_price - payload.unit_variable_cost
    )
    incremental_margin = new_margin - baseline_margin

    return PriceImpactResult(
        volume_factor=volume_factor,
        new_units=new_units,
        new_revenue=new_revenue,
        new_margin=new_margin,
        incremental_margin=incremental_margin,
    )
