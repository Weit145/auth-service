import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from ..config import settings


from alembic.config import Config
from alembic import command


class DatabaseHellper:
    def __init__(self, url: str, echo: bool = False):
        # Создаем асинхронный движок для подключения к БД
        self.engine = create_async_engine(url=url, echo=echo)
        # Создаем фабрику асинхронных сессий
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        # Создаем scoped сессию - одна сессия на одну асинхронную задачу
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=asyncio.current_task
        )
        return session

    @asynccontextmanager
    async def transaction(self):
        session_factory = self.get_scoped_session()
        session = session_factory()
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    @staticmethod
    async def run_migrations():
        for i in range(50):
            try:
                alembic_cfg = Config("alembic.ini")
                await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
                return
            except Exception as e:
                print(f"Database not ready yet ({i + 1}/5): {e}", flush=True)
                await asyncio.sleep(20)

    # @property
    # @staticmethod


db_helper = DatabaseHellper(url=settings.db_url, echo=settings.db_echo)
