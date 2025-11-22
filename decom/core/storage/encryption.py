from cryptography.fernet import Fernet

class EncryptionManager:
    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def encrypt_file(file_path: str, key: bytes) -> str:
        f = Fernet(key)
        with open(file_path, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        
        output_path = file_path + ".enc"
        with open(output_path, "wb") as file:
            file.write(encrypted_data)
        return output_path

    @staticmethod
    def decrypt_file(file_path: str, key: bytes) -> str:
        f = Fernet(key)
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        
        output_path = file_path.replace(".enc", "")
        with open(output_path, "wb") as file:
            file.write(decrypted_data)
        return output_path
