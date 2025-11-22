import jwt
import time
from typing import Dict, Optional

class AuthManager:
    def __init__(self, secret_key: str = "CHANGE_ME", algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.api_keys: Dict[str, str] = {} # api_key -> user_id

    def generate_token(self, user_id: str, role: str, expires_in: int = 3600) -> str:
        """Generate a JWT token."""
        payload = {
            "sub": user_id,
            "role": role,
            "exp": time.time() + expires_in
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token")
            return None

    def create_api_key(self, user_id: str) -> str:
        """Create a simple API key for a user."""
        import secrets
        key = secrets.token_urlsafe(32)
        self.api_keys[key] = user_id
        return key

    def validate_api_key(self, api_key: str) -> Optional[str]:
        """Validate API key and return user_id."""
        return self.api_keys.get(api_key)
