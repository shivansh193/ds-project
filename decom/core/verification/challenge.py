import time
from typing import Dict, Optional
from pydantic import BaseModel

class Challenge(BaseModel):
    id: str
    result_id: str
    challenger_id: str
    reason: str
    status: str = "open" # open, resolved, rejected
    created_at: float = time.time()
    resolved_at: Optional[float] = None

class ChallengeSystem:
    def __init__(self, challenge_period: int = 86400):
        self.challenges: Dict[str, Challenge] = {}
        self.challenge_period = challenge_period # seconds

    def raise_challenge(self, result_id: str, challenger_id: str, reason: str) -> Challenge:
        """Raise a challenge against a result."""
        challenge_id = f"ch_{len(self.challenges) + 1}"
        challenge = Challenge(
            id=challenge_id,
            result_id=result_id,
            challenger_id=challenger_id,
            reason=reason
        )
        self.challenges[challenge_id] = challenge
        print(f"Challenge {challenge_id} raised against result {result_id} by {challenger_id}")
        return challenge

    def resolve_challenge(self, challenge_id: str, outcome: str) -> bool:
        """Resolve a challenge (outcome: 'upheld' or 'rejected')."""
        if challenge_id not in self.challenges:
            return False
        
        challenge = self.challenges[challenge_id]
        if challenge.status != "open":
            return False

        challenge.status = "resolved" if outcome == "upheld" else "rejected"
        challenge.resolved_at = time.time()
        
        print(f"Challenge {challenge_id} resolved: {outcome}")
        return True

    def is_challenge_period_active(self, result_timestamp: float) -> bool:
        return (time.time() - result_timestamp) < self.challenge_period
