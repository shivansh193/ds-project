from typing import List
import time

class Market:
    def __init__(self):
        self.base_price_multiplier = 1.0
        self.last_update = time.time()
        self.demand_history = []

    def update_market_conditions(self, active_bounties: int, active_workers: int):
        """Update market multiplier based on supply and demand."""
        if active_workers == 0:
            self.base_price_multiplier = 2.0 # Surge pricing if no workers
            return

        demand_ratio = active_bounties / active_workers
        
        # Simple dynamic pricing logic
        if demand_ratio > 2.0:
            self.base_price_multiplier = 1.5
        elif demand_ratio > 1.0:
            self.base_price_multiplier = 1.2
        else:
            self.base_price_multiplier = 1.0
            
        self.demand_history.append({
            "timestamp": time.time(),
            "ratio": demand_ratio,
            "multiplier": self.base_price_multiplier
        })

    def get_current_price_multiplier(self) -> float:
        return self.base_price_multiplier

    def calculate_surge_price(self, base_cost: float) -> float:
        return base_cost * self.base_price_multiplier
