# utils/crypto.py

from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
from typing import Optional
import os

# Load variables from .env
load_dotenv()

def _load_key() -> bytes:
    """
    Load the symmetric encryption key from the SECRET_KEY environment variable.
    """
    key = os.getenv("SECRET_KEY")
    if not key:
        raise RuntimeError(
            "SECRET_KEY not found. "
            "Create a .env file with SECRET_KEY=<your_fernet_key>."
        )
    return key.encode("utf-8") if isinstance(key, str) else key


# Global Fernet instance
_FERNET = Fernet(_load_key())


def encrypt_str(value: Optional[str]) -> Optional[bytes]:
    """
    Encrypt a string and return bytes (good for SQLite BLOB/TEXT).
    Returns None if value is None.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    return _FERNET.encrypt(value.encode("utf-8"))


def decrypt_str(stored_value) -> Optional[str]:
    """
    Decrypt a value from SQLite.

    - If encrypted: decrypt normally.
    - If plaintext: return as-is.
    """
    if stored_value is None:
        return None

    if isinstance(stored_value, (bytes, bytearray)):
        raw = bytes(stored_value)
    else:
        raw = str(stored_value).encode("utf-8")

    try:
        return _FERNET.decrypt(raw).decode("utf-8")
    except InvalidToken:
        # Probably plaintext
        try:
            return raw.decode("utf-8")
        except Exception:
            return str(stored_value)
