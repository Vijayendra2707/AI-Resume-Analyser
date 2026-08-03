import os
import bcrypt # 🔴 We use the library directly now
from datetime import datetime, timedelta
from jose import jwt

# --- CONFIGURATION ---
SECRET_KEY = os.getenv("SECRET_KEY", "your_fallback_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- HASHING HELPERS (MODERN BCRYPT) ---

def get_password_hash(password: str):
    """Hashes a password using the bcrypt library directly"""
    # 1. Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Generate a salt
    salt = bcrypt.gensalt()
    # 3. Hash and return as a string for MySQL
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    """Verifies a plain password against the stored hash"""
    try:
        # 1. Convert both to bytes
        pwd_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        # 2. Compare
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception:
        return False

# --- TOKEN GENERATION ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)