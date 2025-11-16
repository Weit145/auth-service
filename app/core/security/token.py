from datetime import UTC, datetime, timedelta

import jwt

from app.core.config import settings


def create_access_token_user(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt

def create_access_token_email(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_email_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt

def create_refresh_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.access_token_refresh_day)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_jwt_username(
    token: str,
)->str|None:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    username = payload.get("sub")
    return username

def decode_jwt_email(
    token: str,
)->str|None:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    email = payload.get("sub")
    return email
