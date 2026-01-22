from pydantic import BaseModel

class Register(BaseModel):
    device_id: str
    account_name: str
    password: str

class Login(BaseModel):
    device_id: str
    account_name: str
    password: str
    totp_code: str
