from dataclasses import dataclass, field
from typing import List, Optional

from src.domain.value_objects import (
    Email,
    Username,
    PasswordHash,
    RefreshToken,
)

from src.domain.events.user_events import (
    UserCreatedEvent,
    UserRegistredEvent,
    UserRefreshedEvent,
    UserAuthenticateEvent,
    UserCurrentedEvent,
)


@dataclass
class User:
    username: Username
    email: Email
    password_hash: PasswordHash
    refresh_token_hash: Optional[RefreshToken] = None
    is_active: bool = True
    is_verified: bool = False
    role: str = "user"

    _events: List[object] = field(default_factory=list, repr=False, compare=False)

    @classmethod
    def create(
        cls,
        username: Username,
        email: Email,
        password_hash: PasswordHash,
        refresh_token_hash: Optional[RefreshToken] = None,
        is_active: bool = True,
        is_verified: bool = False,
        role: str = "user",
    ) -> "User":
        user = cls(
            username=username,
            email=email,
            password_hash=password_hash,
            refresh_token_hash=refresh_token_hash,
            is_active=is_active,
            is_verified=is_verified,
            role=role,
        )
        user._add_event(UserCreatedEvent)
        return user

    def register(self, new_refresh_token_hash: RefreshToken) -> None:
        self.refresh_token_hash = new_refresh_token_hash
        self.is_verified = True
        self._add_event(UserRegistredEvent)

    def refresh_token(self, new_refresh_token_hash: RefreshToken) -> None:
        self.refresh_token_hash = new_refresh_token_hash
        self._add_event(UserRefreshedEvent)

    def authenticate(self, new_refresh_token_hash: RefreshToken) -> None:
        self.refresh_token_hash = new_refresh_token_hash
        self._add_event(UserAuthenticateEvent)

    def current_user(self) -> None:
        self._add_event(UserCurrentedEvent)

    def pull_events(self) -> List[object]:
        events = self._events.copy()
        self._events.clear()
        return events

    def _add_event(self, event: object) -> None:
        self._events.append(event)
