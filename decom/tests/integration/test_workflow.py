import pytest
from decom.core.coordinator.bounty_manager import BountyCreate
from decom.core.coordinator.bid_manager import BidManager
from decom.core.pricing.calculator import PricingCalculator

# Mocking the flow for now as we don't have a running server in this test environment
def test_full_workflow():
    # 1. Create Bounty
    bounty_data = BountyCreate(file_path="test.py", budget=100.0)
    assert bounty_data.budget == 100.0
    
    # 2. Estimate Cost
    calculator = PricingCalculator()
    code = "print('hello world')"
    cost = calculator.estimate_cost(code)
    assert cost["estimated_cost"] > 0
    
    # 3. Place Bid
    bid_manager = BidManager()
    bid = bid_manager.place_bid("b1", "w1", 90.0, 10)
    assert bid.status == "pending"
    
    # 4. Accept Bid
    accepted_bid = bid_manager.accept_bid(bid.id)
    assert accepted_bid.status == "accepted"
    
    print("Workflow test passed!")

if __name__ == "__main__":
    test_full_workflow()
