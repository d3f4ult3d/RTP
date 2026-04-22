from schemas import ReactionInput
from utils import clamp


def _normalize_input(data) -> ReactionInput:
    if isinstance(data, ReactionInput):
        return data
    if isinstance(data, dict):
        return ReactionInput(**data)
    raise TypeError("data must be a ReactionInput instance or a dictionary")


def calculate_reaction_proxy(data: ReactionInput):
    data = _normalize_input(data)

    # Derived variables
    time_available = data.distance / data.ball_speed
    effective_movement_time = max(0, data.event_time - data.movement_start_delay)

    efficiency_ratio = clamp(effective_movement_time / time_available, 0, 1.5)

    # Reaction score (weighted)
    timing_score = clamp(1 - (data.movement_start_delay / time_available), 0, 1)
    base_score = 0.7 * efficiency_ratio + 0.3 * timing_score

    # Outcome boost (reward successful catch slightly)
    if data.outcome == 1:
        base_score += 0.1

    reaction_score = clamp(base_score, 0, 1)

    # Pressure index
    pressure_index = clamp((1 - (time_available / data.event_time)) * 100, 0, 100)

    # Verdict
    if reaction_score > 0.8:
        verdict = "Elite"
    elif reaction_score > 0.6:
        verdict = "Good"
    elif reaction_score > 0.4:
        verdict = "Average"
    else:
        verdict = "Poor"

    return {
        "reaction_score": round(reaction_score, 3),
        "pressure_index": round(pressure_index, 2),
        "verdict": verdict
    }
