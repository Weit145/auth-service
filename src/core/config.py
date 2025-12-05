import os
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv
from passlib.context import CryptContext
from pydantic_settings import BaseSettings

load_dotenv()

class Setting(BaseSettings):
    db_url: str = os.getenv("DB_URL", "sqlite+aiosqlite:///:memory:")
    db_echo: bool = False

    secret_key: str = os.getenv("SECRET_KEY", "default-secret-key")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    access_token_email_minutes: int  = int(os.getenv("ACCESS_TOKEN_EMAIL_MINUTES", "30"))
    access_token_refresh_day: int = int(os.getenv("ACCESS_TOKEN_REFRESH_DAY", "30"))
    algorithm: str = os.getenv("ALGORITHM", "default_alorithm")
    pwd_context: ClassVar[CryptContext] = CryptContext(
        schemes=["argon2"], deprecated="auto"
    )

    kafka_url: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:9092")

settings = Setting()
