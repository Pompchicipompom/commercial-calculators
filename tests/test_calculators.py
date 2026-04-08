"""Basic unit tests for MVP calculators."""

import pytest

from calculators.presence_calculator import calculate_presence_uplift
from calculators.price_impact_calculator import calculate_price_impact
from calculators.promo_roi_calculator import calculate_promo_roi
from calculators.scenario_calculator import ScenarioInput, calculate_unified_scenario
from models.presence_model import PresenceInput
from models.price_model import PriceInput
from models.promo_model import PromoInput


def test_presence_uplift_positive() -> None:
    payload = PresenceInput(
        baseline_units=1000,
        current_in_stock=0.8,
        target_in_stock=0.9,
        beta_presence=1.0,
        cap_uplift_pct=0.5,
    )
    result = calculate_presence_uplift(payload)
    assert result.uplift_pct == pytest.approx(0.1)
    assert result.incremental_units == pytest.approx(100.0)
    assert result.projected_units == pytest.approx(1100.0)


def test_promo_roi_basic_case() -> None:
    payload = PromoInput(
        baseline_units=1000,
        promo_units=1300,
        promo_price=100,
        unit_variable_cost=60,
        promo_cost_fixed=6000,
        promo_cost_variable=2000,
    )
    result = calculate_promo_roi(payload)
    # Incremental margin = 300 * 40 = 12000, net effect = 4000, ROI = 0.5
    assert result.incremental_margin == pytest.approx(12000.0)
    assert result.net_effect == pytest.approx(4000.0)
    assert result.roi == pytest.approx(0.5)


def test_price_impact_negative_elasticity_on_price_increase() -> None:
    payload = PriceInput(
        baseline_units=1000,
        old_price=100,
        new_price=110,
        elasticity=-1.2,
        unit_variable_cost=60,
    )
    result = calculate_price_impact(payload)
    assert result.volume_factor < 1.0
    assert result.new_units < 1000


def test_unified_scenario_combines_effects() -> None:
    presence = PresenceInput(
        baseline_units=1000,
        current_in_stock=0.85,
        target_in_stock=0.95,
        beta_presence=1.0,
        cap_uplift_pct=0.5,
    )
    promo = PromoInput(
        baseline_units=1000,
        promo_units=1200,
        promo_price=95,
        unit_variable_cost=60,
        promo_cost_fixed=5000,
        promo_cost_variable=1000,
    )
    price = PriceInput(
        baseline_units=1000,
        old_price=100,
        new_price=102,
        elasticity=-1.0,
        unit_variable_cost=60,
    )
    payload = ScenarioInput(
        baseline_units=1000,
        baseline_price=100,
        unit_variable_cost=60,
        promo_share_of_period=0.5,
        overlap_coeff=0.85,
        presence_input=presence,
        promo_input=promo,
        price_input=price,
    )
    result = calculate_unified_scenario(payload)
    assert result.adjusted_volume_factor > 0
    assert result.scenario_units > 0
    assert result.scenario_revenue > 0
