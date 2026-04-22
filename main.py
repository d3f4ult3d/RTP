from fastapi import FastAPI, HTTPException
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
