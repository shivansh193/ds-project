from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid

app = FastAPI(title="Decom Coordinator")

# In-memory storage for MVP
bounties: Dict[str, dict] = {}

class BountyCreate(BaseModel):
    ipfs_cid: str
    complexity_score: int
    estimated_cost: float
    filename: str

class Bounty(BountyCreate):
    id: str
    status: str  # PENDING, IN_PROGRESS, COMPLETED
    worker_id: Optional[str] = None
    decryption_key: Optional[str] = None
    result_key: Optional[str] = None
    result_ipfs_cid: Optional[str] = None

class KeySubmission(BaseModel):
    key: str
    result_key: str

class ResultSubmission(BaseModel):
    ipfs_cid: str

@app.post("/bounties", response_model=Bounty)
def create_bounty(bounty: BountyCreate):
    bounty_id = str(uuid.uuid4())
    new_bounty = {
        "id": bounty_id,
        **bounty.dict(),
        "status": "PENDING",
        "worker_id": None,
        "decryption_key": None,
        "result_key": None,
        "result_ipfs_cid": None
    }
    bounties[bounty_id] = new_bounty
    return new_bounty

@app.get("/bounties", response_model=List[Bounty])
def list_bounties(status: Optional[str] = None):
    if status:
        return [b for b in bounties.values() if b["status"] == status]
    return list(bounties.values())

@app.get("/bounties/{bounty_id}", response_model=Bounty)
def get_bounty(bounty_id: str):
    if bounty_id not in bounties:
        raise HTTPException(status_code=404, detail="Bounty not found")
    return bounties[bounty_id]

@app.post("/bounties/{bounty_id}/accept")
def accept_bounty(bounty_id: str, worker_id: str):
    if bounty_id not in bounties:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    bounty = bounties[bounty_id]
    if bounty["status"] != "PENDING":
        raise HTTPException(status_code=400, detail="Bounty already accepted or completed")
    
    bounty["status"] = "IN_PROGRESS"
    bounty["worker_id"] = worker_id
    return {"message": "Bounty accepted", "bounty": bounty}

@app.post("/bounties/{bounty_id}/key")
def submit_key(bounty_id: str, submission: KeySubmission):
    if bounty_id not in bounties:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    # In a real app, verify sender is the creator
    bounties[bounty_id]["decryption_key"] = submission.key
    bounties[bounty_id]["result_key"] = submission.result_key
    return {"message": "Keys received"}

@app.get("/bounties/{bounty_id}/key")
def get_key(bounty_id: str, worker_id: str):
    if bounty_id not in bounties:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    bounty = bounties[bounty_id]
    # In a real app, verify worker_id matches assigned worker
    if not bounty["decryption_key"]:
        raise HTTPException(status_code=404, detail="Key not yet available")
        
    return {
        "key": bounty["decryption_key"],
        "result_key": bounty["result_key"]
    }

@app.post("/bounties/{bounty_id}/result")
def submit_result(bounty_id: str, submission: ResultSubmission):
    if bounty_id not in bounties:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    bounty = bounties[bounty_id]
    bounty["status"] = "COMPLETED"
    bounty["result_ipfs_cid"] = submission.ipfs_cid
    return {"message": "Result received"}
