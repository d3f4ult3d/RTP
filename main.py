import json
import sys

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from schemas import ReactionInput, ReactionOutput
from services import calculate_reaction_proxy

app = FastAPI(title="Reaction Time Proxy API")

@app.post("/predict/reaction", response_model=ReactionOutput)
def predict_reaction(data: ReactionInput):
    try:
        return calculate_reaction_proxy(data)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.get("/health")
def health_check():
    return {"status": "ok"}


def _prompt_number(label: str, cast=float):
    while True:
        raw = input(f"{label}: ").strip()
        try:
            return cast(raw)
        except ValueError:
            print("Enter a valid number.")


def run_raw_input_cli() -> None:
    print("\nReaction Time Proxy raw input calculator\n")
    try:
        data = ReactionInput(
            ball_speed=_prompt_number("Ball speed"),
            distance=_prompt_number("Distance"),
            event_time=_prompt_number("Event time"),
            movement_start_delay=_prompt_number("Movement start delay"),
            outcome=_prompt_number("Outcome 0 or 1", int),
        )
        output = ReactionOutput(**calculate_reaction_proxy(data))
    except ValidationError as exc:
        print("\nInput validation error:")
        for error in exc.errors():
            field = ".".join(str(part) for part in error["loc"])
            print(f"- {field}: {error['msg']}")
        return

    print("\nRTP output")
    print(f"Reaction score: {output.reaction_score}")
    print(f"Pressure index: {output.pressure_index}")
    print(f"Verdict: {output.verdict}")
    print("\nFull response:")
    print(json.dumps(output.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    if "--api" in sys.argv:
        import uvicorn

        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        run_raw_input_cli()
