from typing import Dict, Optional
from pydantic import BaseModel

class Transaction(BaseModel):
    id: str
    user_id: str
    amount: float
    type: str # deposit, withdraw, escrow, release, refund
    timestamp: float

class PaymentProcessor:
    def __init__(self):
        self.balances: Dict[str, float] = {} # user_id -> balance
        self.transactions: list[Transaction] = []

    def get_balance(self, user_id: str) -> float:
        return self.balances.get(user_id, 0.0)

    def deposit(self, user_id: str, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        current = self.get_balance(user_id)
        self.balances[user_id] = current + amount
        # Log transaction
        return self.balances[user_id]

    def withdraw(self, user_id: str, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        current = self.get_balance(user_id)
        if current < amount:
            return False
        
        self.balances[user_id] = current - amount
        return True

    def escrow_funds(self, user_id: str, amount: float) -> bool:
        """Lock funds for a bounty."""
        # For MVP, just deduct from balance. In real system, move to escrow account.
        return self.withdraw(user_id, amount)

    def release_funds(self, worker_id: str, amount: float):
        """Release funds to a worker."""
        self.deposit(worker_id, amount)
