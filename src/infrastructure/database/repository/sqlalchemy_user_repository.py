from sqlalchemy import select


from domain.entities.user import User
from domain.value_objects import (
    Email,
    Username,
)
from infrastructure.database.models.user_orm_model import UserORM
from src.domain.repositories.iuser_repository import IUserRepository
from src.infrastructure.db_hellper import db_helper
from src.infrastructure.database.utils.convert import (
    convert_orm_to_user,
    convert_user_to_orm
)

class SQLAlchemyAuthRepository(IUserRepository):

    async def add(self, user: User) -> User:
        user_orm = convert_user_to_orm(user)
        try:
            async with db_helper.transaction() as session:
                session.add(user_orm)
                return user
        except Exception as e:
            raise e
    
    async def get_by_username(self, username: Username) -> User | None:
        try:
            async with db_helper.transaction() as session:
                result = await session.execute(select(UserORM).where(UserORM.username==username))
                return convert_orm_to_user(result.scalar_one_or_none())
        except Exception as e:
            raise e
    
    async def get_by_email(self, email: Email) -> User | None:
        try:
            async with db_helper.transaction() as session:
                result = await session.execute(select(UserORM).where(UserORM.email==email))
                return convert_orm_to_user(result.scalar_one_or_none())
        except Exception as e:
            raise e
    
    async def update(self, user: User) -> User:
        try:
            user_orm = convert_user_to_orm(user)
            async with db_helper.transaction() as session:
                session.add(user_orm)
                return user
        except Exception as e:
            raise e
    
    async def delete(self, user: User) -> None:
        try:
            user_orm = convert_user_to_orm(user)
            async with db_helper.transaction() as session:
                await session.delete(user_orm)
        except Exception as e:
            raise e