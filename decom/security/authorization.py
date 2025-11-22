from typing import List, Dict

class RBAC:
    def __init__(self):
        self.roles: Dict[str, List[str]] = {
            "admin": ["create_bounty", "cancel_bounty", "place_bid", "verify_result", "manage_users"],
            "user": ["create_bounty", "cancel_bounty", "view_bounty"],
            "worker": ["place_bid", "view_bounty", "submit_result"]
        }

    def has_permission(self, role: str, permission: str) -> bool:
        """Check if a role has a specific permission."""
        if role not in self.roles:
            return False
        return permission in self.roles[role]

    def add_role(self, role: str, permissions: List[str]):
        self.roles[role] = permissions
