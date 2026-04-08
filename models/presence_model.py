"""Pydantic schemas for presence uplift modeling."""

from pydantic import BaseModel, Field


class PresenceInput(BaseModel):
    """Input payload for presence uplift calculations."""

    baseline_units: float = Field(gt=0, description="Baseline sales volume in units.")
    current_in_stock: float = Field(
        ge=0, le=1, description="Current in-stock rate as a share (0..1)."
    )
    target_in_stock: float = Field(
        ge=0, le=1, description="Target in-stock rate as a share (0..1)."
    )
    beta_presence: float = Field(
        gt=0, le=3, description="Semi-elasticity coefficient for presence impact."
    )
    cap_uplift_pct: float = Field(
        default=0.5, ge=0, le=2, description="Optional cap for uplift percent (0..2)."
    )


class PresenceResult(BaseModel):
    """Result of presence uplift calculations."""

    uplift_pct: float = Field(ge=0)
    incremental_units: float
    projected_units: float
