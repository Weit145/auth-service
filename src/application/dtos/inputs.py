from dataclasses import dataclass


@dataclass
class CreateUserInput:
    username: str
    email: str
    password: str


@dataclass
class ConfirmUserInput:
    token: str


@dataclass
class RefreshTokenInput:
    refresh_token: str


@dataclass
class LoginUserInput:
    username: str
    password: str


@dataclass
class CurrentUserInput:
    username: str
