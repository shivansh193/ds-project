from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class BountyCreate(BaseModel):
    file_path: str
    budget: float
    timeout: int = 3600
    redundancy: int = 3

class Bounty(BaseModel):
    id: str
    status: str
    budget: float

# In-memory storage for MVP
bounties_db = []

@router.post("/", response_model=Bounty)
async def create_bounty(bounty: BountyCreate):
    new_bounty = {
        "id": str(len(bounties_db) + 1),
        "status": "pending",
        "budget": bounty.budget
    }
    bounties_db.append(new_bounty)
    return new_bounty

@router.get("/", response_model=List[Bounty])
async def list_bounties():
    return bounties_db

@router.get("/{bounty_id}", response_model=Bounty)
async def get_bounty(bounty_id: str):
    for b in bounties_db:
        if b["id"] == bounty_id:
            return b
    raise HTTPException(status_code=404, detail="Bounty not found")
