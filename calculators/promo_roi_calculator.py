"""Calculator for promo ROI and break-even uplift."""

from models.promo_model import PromoInput, PromoResult


def calculate_promo_roi(payload: PromoInput) -> PromoResult:
    """
    Calculate promo ROI using incremental contribution margin.

    Simplified MVP logic:
    - incremental_units = promo_units - baseline_units
    - incremental_margin = incremental_units * (promo_price - unit_variable_cost)
    - roi = (incremental_margin - promo_total_cost) / promo_total_cost
    """

    incremental_units = payload.promo_units - payload.baseline_units
    unit_margin = payload.promo_price - payload.unit_variable_cost
    incremental_margin = incremental_units * unit_margin

    promo_total_cost = payload.promo_cost_fixed + payload.promo_cost_variable
    net_effect = incremental_margin - promo_total_cost

    if promo_total_cost > 0:
        roi = net_effect / promo_total_cost
    else:
        roi = float("inf") if net_effect > 0 else 0.0

    if unit_margin > 0:
        break_even_incremental_units = promo_total_cost / unit_margin
    else:
        break_even_incremental_units = float("inf")

    return PromoResult(
        incremental_units=incremental_units,
        incremental_margin=incremental_margin,
        promo_total_cost=promo_total_cost,
        net_effect=net_effect,
        roi=roi,
        break_even_incremental_units=break_even_incremental_units,
    )
