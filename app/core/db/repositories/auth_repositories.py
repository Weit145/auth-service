import grpc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db_hellper import db_helper
from ..models.auth import Auth
from .iauth_repositories import IAuthRepository


class SQLAlchemyAuthRepository(IAuthRepository):

    async def create_auth_user(self, user: Auth,context) -> None:
        try:
            async with db_helper.transaction() as session:
                session.add(user)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def activate_user_with_refresh(self, user: Auth,refresh_token: str,context) -> None:
        user.is_verified = True
        user.refresh_token_hash = refresh_token
        try:
            async with db_helper.transaction() as session:
                session.add(user)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def add_refresh_token(self, user: Auth, refresh_token: str,context) -> None:
        user.refresh_token_hash = refresh_token
        try:
            async with db_helper.transaction() as session:
                session.add(user)
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

    async def get_user_by_login(self, login: str,context) -> Auth | None:
        async with db_helper.transaction() as session:
            result = await session.execute(select(Auth).where(Auth.login==login))
            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str,context) -> Auth | None:
        async with db_helper.transaction() as session:
            result = await session.execute(select(Auth).filter(Auth.email == email))
            return result.scalar_one_or_none()
    
    async def get_user_by_id(self, id: int) -> Auth | None:
        async with db_helper.transaction() as session:
            result = await session.get(Auth,id)
            return result

    async def delete_auth_user(self, user: Auth) -> None:
        async with db_helper.transaction() as session:
            await session.delete(user)

    async def update_auth_user(self, user: Auth,context) -> None:
        async with db_helper.transaction() as session:
            session.add(user)
