import pyotp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from app.database import SessionLocal
from app.models import User
from app.security import hash_password, encrypt_secret
from app.config import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(prefix="/owner")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def owner_only(token: str):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    if payload.get("role") != "owner":
        raise HTTPException(403)

@router.get("/users")
def list_users(token: str, db: Session = Depends(get_db)):
    owner_only(token)
    return db.query(User).all()

@router.post("/reset-password/{user_id}")
def reset_password(user_id: str, new_password: str, token: str, db: Session = Depends(get_db)):
    owner_only(token)
    user = db.query(User).get(user_id)
    user.password_hash = hash_password(new_password)
    db.commit()
    return {"status": "password reset"}

@router.post("/rotate-totp/{user_id}")
def rotate_totp(user_id: str, token: str, db: Session = Depends(get_db)):
    owner_only(token)
    user = db.query(User).get(user_id)
    new_secret = pyotp.random_base32()
    user.totp_secret_encrypted = encrypt_secret(new_secret)
    db.commit()
    uri = pyotp.totp.TOTP(new_secret).provisioning_uri(
        name=user.account_name,
        issuer_name="SecureAuthenticator"
    )
    return {"new_qr_uri": uri}
