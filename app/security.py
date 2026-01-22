from passlib.context import CryptContext
from cryptography.fernet import Fernet
from jose import jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, FERNET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cipher = Fernet(FERNET_KEY.encode())

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def encrypt_secret(secret: str) -> str:
    return cipher.encrypt(secret.encode()).decode()

def decrypt_secret(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()

def create_jwt(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
