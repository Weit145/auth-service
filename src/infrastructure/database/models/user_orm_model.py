from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class UserORM(DeclarativeBase):
    __tablename__ = "auth"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(nullable=False, unique=True)  
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    refresh_token_hash: Mapped[str] = mapped_column(server_default=text("0"))
    is_active: Mapped[bool] = mapped_column(server_default=text("True"))
    is_verified: Mapped[bool] = mapped_column(server_default=text("False"))
    role: Mapped[str] = mapped_column(nullable=False, default="user")