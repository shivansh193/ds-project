from typing import List, Dict, Optional
from pydantic import BaseModel
import time

class Bid(BaseModel):
    id: str
    bounty_id: str
    worker_id: str
    price: float
    eta: int  # minutes
    status: str = "pending"  # pending, accepted, rejected
    timestamp: float = time.time()

class BidManager:
    def __init__(self):
        self.bids: Dict[str, Bid] = {}

    def place_bid(self, bounty_id: str, worker_id: str, price: float, eta: int) -> Bid:
        """Place a new bid on a bounty."""
        bid_id = f"bid_{len(self.bids) + 1}"
        bid = Bid(
            id=bid_id,
            bounty_id=bounty_id,
            worker_id=worker_id,
            price=price,
            eta=eta
        )
        # TODO: Validate worker reputation and price range
        self.bids[bid_id] = bid
        return bid

    def get_bids_for_bounty(self, bounty_id: str) -> List[Bid]:
        """Get all bids for a specific bounty."""
        return [bid for bid in self.bids.values() if bid.bounty_id == bounty_id]

    def accept_bid(self, bid_id: str) -> Optional[Bid]:
        """Accept a bid and reject others for the same bounty (if single worker)."""
        if bid_id not in self.bids:
            return None
        
        bid = self.bids[bid_id]
        if bid.status != "pending":
            return None # Already processed

        bid.status = "accepted"
        # Logic to reject other bids or handle redundancy would go here
        return bid

    def reject_bid(self, bid_id: str) -> Optional[Bid]:
        """Reject a specific bid."""
        if bid_id not in self.bids:
            return None
        
        bid = self.bids[bid_id]
        bid.status = "rejected"
        return bid

    def rank_bids(self, bounty_id: str) -> List[Bid]:
        """Rank bids based on price and ETA."""
        bids = self.get_bids_for_bounty(bounty_id)
        # Simple ranking: lowest price, then lowest ETA
        return sorted(bids, key=lambda x: (x.price, x.eta))
