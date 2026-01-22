import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    totp_secret_encrypted = Column(String, nullable=False)
    role = Column(String, default="user")
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
