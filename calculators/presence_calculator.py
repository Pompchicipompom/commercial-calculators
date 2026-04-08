"""Calculator for presence-driven uplift."""

from models.presence_model import PresenceInput, PresenceResult


def calculate_presence_uplift(payload: PresenceInput) -> PresenceResult:
    """
    Calculate uplift from better on-shelf availability.

    Formula:
    uplift_pct = min(beta_presence * max(target_in_stock - current_in_stock, 0), cap_uplift_pct)
    incremental_units = baseline_units * uplift_pct
    """

    delta_in_stock = max(payload.target_in_stock - payload.current_in_stock, 0.0)
    uplift_pct = min(payload.beta_presence * delta_in_stock, payload.cap_uplift_pct)
    incremental_units = payload.baseline_units * uplift_pct
    projected_units = payload.baseline_units + incremental_units

    return PresenceResult(
        uplift_pct=uplift_pct,
        incremental_units=incremental_units,
        projected_units=projected_units,
    )
