from fastapi import FastAPI
from app.auth import router as auth_router
from app.owner import router as owner_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Authenticator")
app.include_router(auth_router)
app.include_router(owner_router)
