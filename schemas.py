from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

class ReactionInput(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    ball_speed: float = Field(..., gt=0, allow_inf_nan=False)
    distance: float = Field(..., gt=0, allow_inf_nan=False)
    event_time: float = Field(..., gt=0, allow_inf_nan=False)
    movement_start_delay: float = Field(..., ge=0, allow_inf_nan=False)
    outcome: int = Field(..., ge=0, le=1, strict=True)

    @model_validator(mode="after")
    def validate_timing(self):
        if self.movement_start_delay > self.event_time:
            raise ValueError("movement_start_delay cannot be greater than event_time")
        return self

class ReactionOutput(BaseModel):
    reaction_score: float = Field(..., ge=0, le=1, allow_inf_nan=False)
    pressure_index: float = Field(..., ge=0, le=100, allow_inf_nan=False)
    verdict: Literal["Elite", "Good", "Average", "Poor"]
