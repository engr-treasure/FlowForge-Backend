from fastapi import Depends
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta
from jose import jwt
from app.core.config import settings
from sqlalchemy.orm import Session


password_hash = PasswordHash.recommended()
ALGORITHM = "HS256"

def encrypt_password(password: str) -> str:
    hashed_password = password_hash.hash(password)
    return hashed_password

def verify_password(password: str, db_password: str) -> bool:
    verified_password = password_hash.verify(
        password,
        db_password
    )
    return verified_password

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_data = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=ALGORITHM
    )
    return encoded_data

def decode_access_token(
        token: str
):
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=ALGORITHM
    )
    return payload

    