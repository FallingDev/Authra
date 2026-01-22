# Secure Authenticator Backend

## Features
- Password + TOTP authentication
- Owner/admin account
- Encrypted secrets
- JWT auth
- PostgreSQL
- Fly.io ready

## Run locally
pip install -r requirements.txt
uvicorn app.main:app --reload
