from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db_hellper import db_helper
from ..models.auth import Auth
from .iauth_repositories import IAuthRepository


class SQLAlchemyAuthRepository(IAuthRepository):

    async def create_auth_user(self, user: Auth) -> str:
        try:
            async with db_helper.transaction() as session:
                session.add(user)
                return ""
        except Exception as e:
            return str(e)

    async def activate_user_with_refresh(self, user: Auth,refresh_token: str) -> str:
        user.is_verified = True
        user.refresh_token_hash = refresh_token
        try:
            async with db_helper.transaction() as session:
                session.add(user)
                return ""
        except Exception as e:
            return str(e)

    async def add_refresh_token(self, user: Auth, refresh_token: str) -> str:
        user.refresh_token_hash = refresh_token
        try:
            async with db_helper.transaction() as session:
                session.add(user)
                return ""
        except Exception as e:
            return str(e)

    async def get_user_by_username(self, username: str) -> Auth | None:
        async with db_helper.transaction() as session:
            result = await session.execute(select(Auth).where(Auth.username==username))
            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Auth | None:
        async with db_helper.transaction() as session:
            result = await session.execute(select(Auth).filter(Auth.email == email))
            return result.scalar_one_or_none()

    async def delete_auth_user(self, user: Auth) -> None:
        async with db_helper.transaction() as session:
            await session.delete(user)

    async def update_auth_user(self, user: Auth) -> None:
        async with db_helper.transaction() as session:
            session.add(user)
