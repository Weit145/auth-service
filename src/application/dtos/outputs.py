from dataclasses import dataclass
from os import access

@dataclass
class Cookie:
    key: str
    value: str
    httponly: bool
    secure: bool
    samesite: str
    max_age: int

@dataclass
class CookieOutput:
    access_token: str
    cookie : Cookie

@dataclass
class TokenOutput:
    access_token: str

@dataclass
class UserOutput:
    username: str
    is_active: bool
    is_verified: bool
    role: str