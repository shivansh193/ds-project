from fastapi import FastAPI
from decom.core.coordinator.bounty_manager import router as bounty_router

app = FastAPI(title="DeCom Coordinator", version="0.1.0")

app.include_router(bounty_router, prefix="/api/v1/bounties", tags=["bounties"])

@app.get("/")
async def root():
    return {"message": "DeCom Coordinator Running"}

@app.get("/api/v1/stats")
async def stats():
    return {"workers": 5, "bounties": 10}
