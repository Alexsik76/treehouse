from cryptography.fernet import Fernet
from src.config import settings

# Створення об'єкта Fernet при запуску (ключ має бути валідним base64)
cipher_suite = Fernet(settings.ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """
    Encrypts a string and returns the encrypted token as a string.
    """
    if not data:
        return ""
    # Fernet encrypt expects bytes, so we encode the string
    encrypted_bytes = cipher_suite.encrypt(data.encode("utf-8"))
    # We return the encrypted token as a string to store in DB
    return encrypted_bytes.decode("utf-8")

def decrypt_data(token: str) -> str:
    """
    Decrypts an encrypted token string and returns the original string.
    """
    if not token:
        return ""
    # Fernet decrypt expects bytes
    decrypted_bytes = cipher_suite.decrypt(token.encode("utf-8"))
    return decrypted_bytes.decode("utf-8")
