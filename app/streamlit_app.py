"""Skeleton Streamlit application for commercial calculators MVP."""

from pathlib import Path
import sys

import streamlit as st
from pydantic import ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from calculators.presence_calculator import calculate_presence_uplift
from calculators.price_impact_calculator import calculate_price_impact
from calculators.promo_roi_calculator import calculate_promo_roi
from calculators.scenario_calculator import (
    ScenarioInput,
    calculate_unified_scenario,
)
from config import settings
from models.presence_model import PresenceInput
from models.price_model import PriceInput
from models.promo_model import PromoInput


def render_presence_page() -> None:
    """Render UI for presence uplift calculator."""
    st.subheader("Presence Uplift")

    baseline_units = st.number_input("Baseline units", min_value=1.0, value=1000.0)
    current_in_stock = st.slider("Current in-stock", 0.0, 1.0, 0.85, 0.01)
    target_in_stock = st.slider("Target in-stock", 0.0, 1.0, 0.95, 0.01)
    beta_presence = st.number_input(
        "Presence beta",
        min_value=0.01,
        max_value=3.0,
        value=settings.default_presence_beta,
    )

    if st.button("Calculate presence uplift"):
        try:
            payload = PresenceInput(
                baseline_units=baseline_units,
                current_in_stock=current_in_stock,
                target_in_stock=target_in_stock,
                beta_presence=beta_presence,
                cap_uplift_pct=settings.default_presence_cap_uplift,
            )
            result = calculate_presence_uplift(payload)
            st.metric("Uplift, %", f"{result.uplift_pct * 100:.2f}%")
            st.metric("Incremental units", f"{result.incremental_units:.0f}")
            st.metric("Projected units", f"{result.projected_units:.0f}")
        except ValidationError as exc:
            st.error(str(exc))


def render_promo_page() -> None:
    """Render UI for promo ROI calculator."""
    st.subheader("Promo ROI")

    baseline_units = st.number_input("Baseline units", min_value=1.0, value=1000.0, key="promo_base")
    promo_units = st.number_input("Promo units", min_value=1.0, value=1300.0)
    promo_price = st.number_input("Promo price", min_value=0.01, value=99.0)
    unit_variable_cost = st.number_input("Unit variable cost", min_value=0.01, value=60.0)
    promo_cost_fixed = st.number_input("Promo fixed cost", min_value=0.0, value=10000.0)
    promo_cost_variable = st.number_input("Promo variable cost", min_value=0.0, value=5000.0)

    if st.button("Calculate promo ROI"):
        try:
            payload = PromoInput(
                baseline_units=baseline_units,
                promo_units=promo_units,
                promo_price=promo_price,
                unit_variable_cost=unit_variable_cost,
                promo_cost_fixed=promo_cost_fixed,
                promo_cost_variable=promo_cost_variable,
            )
            result = calculate_promo_roi(payload)
            st.metric("ROI", f"{result.roi:.2f}")
            st.metric("Net effect", f"{result.net_effect:,.0f}")
            st.metric("Break-even incremental units", f"{result.break_even_incremental_units:,.0f}")
        except ValidationError as exc:
            st.error(str(exc))


def render_price_page() -> None:
    """Render UI for price impact calculator."""
    st.subheader("Price Impact")

    baseline_units = st.number_input("Baseline units", min_value=1.0, value=1000.0, key="price_base")
    old_price = st.number_input("Old price", min_value=0.01, value=100.0)
    new_price = st.number_input("New price", min_value=0.01, value=105.0)
    elasticity = st.number_input("Elasticity (<0)", value=-1.2)
    unit_variable_cost = st.number_input("Unit variable cost", min_value=0.01, value=60.0, key="price_cost")

    if st.button("Calculate price impact"):
        try:
            payload = PriceInput(
                baseline_units=baseline_units,
                old_price=old_price,
                new_price=new_price,
                elasticity=elasticity,
                unit_variable_cost=unit_variable_cost,
            )
            result = calculate_price_impact(payload)
            st.metric("Volume factor", f"{result.volume_factor:.3f}")
            st.metric("New units", f"{result.new_units:.0f}")
            st.metric("Incremental margin", f"{result.incremental_margin:,.0f}")
        except ValidationError as exc:
            st.error(str(exc))


def render_scenario_page() -> None:
    """Render UI for unified scenario engine."""
    st.subheader("Unified Scenario")

    baseline_units = st.number_input("Scenario baseline units", min_value=1.0, value=1000.0)
    baseline_price = st.number_input("Scenario baseline price", min_value=0.01, value=100.0)
    unit_variable_cost = st.number_input("Scenario unit variable cost", min_value=0.01, value=60.0)
    overlap_coeff = st.slider("Overlap coefficient", 0.0, 1.0, settings.default_overlap_coeff, 0.01)
    promo_share = st.slider(
        "Promo share of period",
        0.0,
        1.0,
        settings.default_promo_share_of_period,
        0.05,
    )

    st.caption("Optional component inputs")
    use_presence = st.checkbox("Use presence effect", value=True)
    use_promo = st.checkbox("Use promo effect", value=True)
    use_price = st.checkbox("Use price effect", value=True)

    presence_input = None
    promo_input = None
    price_input = None

    if use_presence:
        presence_input = PresenceInput(
            baseline_units=baseline_units,
            current_in_stock=st.slider("Current in-stock (scenario)", 0.0, 1.0, 0.85, 0.01, key="s_cur"),
            target_in_stock=st.slider("Target in-stock (scenario)", 0.0, 1.0, 0.95, 0.01, key="s_tgt"),
            beta_presence=st.number_input(
                "Presence beta (scenario)", min_value=0.01, max_value=3.0, value=settings.default_presence_beta
            ),
            cap_uplift_pct=settings.default_presence_cap_uplift,
        )

    if use_promo:
        promo_input = PromoInput(
            baseline_units=baseline_units,
            promo_units=st.number_input("Promo units (scenario)", min_value=1.0, value=1200.0),
            promo_price=st.number_input("Promo price (scenario)", min_value=0.01, value=95.0),
            unit_variable_cost=unit_variable_cost,
            promo_cost_fixed=st.number_input("Promo fixed cost (scenario)", min_value=0.0, value=8000.0),
            promo_cost_variable=st.number_input("Promo variable cost (scenario)", min_value=0.0, value=4000.0),
        )

    if use_price:
        price_input = PriceInput(
            baseline_units=baseline_units,
            old_price=baseline_price,
            new_price=st.number_input("New price (scenario)", min_value=0.01, value=102.0),
            elasticity=st.number_input("Elasticity (scenario)", value=-1.1),
            unit_variable_cost=unit_variable_cost,
        )

    if st.button("Calculate unified scenario"):
        payload = ScenarioInput(
            baseline_units=baseline_units,
            baseline_price=baseline_price,
            unit_variable_cost=unit_variable_cost,
            promo_share_of_period=promo_share,
            overlap_coeff=overlap_coeff,
            presence_input=presence_input,
            promo_input=promo_input,
            price_input=price_input,
        )
        result = calculate_unified_scenario(payload)
        st.metric("Adjusted volume factor", f"{result.adjusted_volume_factor:.3f}")
        st.metric("Scenario units", f"{result.scenario_units:.0f}")
        st.metric("Scenario ROI", f"{result.scenario_roi:.2f}")
        st.metric("Incremental margin", f"{result.incremental_margin:,.0f}")


def main() -> None:
    """Main entrypoint for the Streamlit application."""
    st.set_page_config(page_title=settings.app_title, layout="wide")
    st.title(settings.app_title)
    st.caption("MVP platform for commercial driver calculators")

    page = st.sidebar.radio(
        "Select calculator",
        ("Presence uplift", "Promo ROI", "Price impact", "Unified scenario"),
    )

    if page == "Presence uplift":
        render_presence_page()
    elif page == "Promo ROI":
        render_promo_page()
    elif page == "Price impact":
        render_price_page()
    else:
        render_scenario_page()


if __name__ == "__main__":
    main()
