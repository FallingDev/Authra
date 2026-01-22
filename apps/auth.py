import pyotp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import Register, Login
from app.security import hash_password, verify_password, encrypt_secret, decrypt_secret, create_jwt

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(data: Register, db: Session = Depends(get_db)):
    secret = pyotp.random_base32()
    user = User(
        device_id=data.device_id,
        account_name=data.account_name,
        password_hash=hash_password(data.password),
        totp_secret_encrypted=encrypt_secret(secret),
        role="user"
    )
    db.add(user)
    db.commit()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=data.account_name,
        issuer_name="SecureAuthenticator"
    )
    return {"qr_uri": uri}

@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(
        device_id=data.device_id,
        account_name=data.account_name
    ).first()
    if not user or user.disabled:
        raise HTTPException(401)
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(401)
    secret = decrypt_secret(user.totp_secret_encrypted)
    if not pyotp.TOTP(secret).verify(data.totp_code):
        raise HTTPException(401)
    token = create_jwt({"sub": str(user.id), "role": user.role})
    return {"access_token": token}
