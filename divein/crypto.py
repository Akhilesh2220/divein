"""
Encryption utilities for DiveIn using PBKDF2 and Fernet (AES).
"""
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(master_password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
    Derive a Fernet-compatible key from the master password.
    Returns the key and the salt used.
    """
    if salt is None:
        salt = os.urandom(16)
        
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key, salt

def encrypt_password(password: str, master_password: str) -> dict:
    """
    Encrypt a password using the master password.
    Returns a dictionary containing the encrypted token and the salt (hex-encoded).
    """
    if not password:
        return {"input_type": "none"}
        
    key, salt = derive_key(master_password)
    f = Fernet(key)
    token = f.encrypt(password.encode())
    
    return {
        "encrypted_data": token.decode(),
        "salt": salt.hex(),
        "input_type": "encrypted_password"
    }

def decrypt_password(encrypted_data: str, salt_hex: str, master_password: str) -> str:
    """
    Decrypt the password using the master password.
    """
    try:
        salt = bytes.fromhex(salt_hex)
        key, _ = derive_key(master_password, salt)
        f = Fernet(key)
        return f.decrypt(encrypted_data.encode()).decode()
    except Exception:
        raise ValueError("Invalid Master Password or corrupted data")
