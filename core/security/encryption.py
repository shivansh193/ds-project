from cryptography.fernet import Fernet
import os

class EncryptionManager:
    @staticmethod
    def generate_key() -> bytes:
        """Generates a new Fernet key."""
        return Fernet.generate_key()

    @staticmethod
    def encrypt_file(file_path: str, key: bytes, data: bytes = None) -> bytes:
        """Encrypts a file or raw data and returns the encrypted bytes."""
        f = Fernet(key)
        if data:
            file_data = data
        else:
            with open(file_path, "rb") as file:
                file_data = file.read()
        return f.encrypt(file_data)

    @staticmethod
    def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
        """Decrypts data using the provided key."""
        f = Fernet(key)
        return f.decrypt(encrypted_data)

    @staticmethod
    def save_encrypted_file(encrypted_data: bytes, output_path: str):
        """Saves encrypted bytes to a file."""
        with open(output_path, "wb") as file:
            file.write(encrypted_data)
