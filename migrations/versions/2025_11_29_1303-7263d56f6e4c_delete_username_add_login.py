"""Delete username add login

Revision ID: 7263d56f6e4c
Revises: 2ca723ecc8c0
Create Date: 2025-11-29 13:03:37.307486

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7263d56f6e4c"
down_revision: Union[str, Sequence[str], None] = "2ca723ecc8c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Удаляем уникальное ограничение на username
    op.drop_constraint("auth_username_key", "auth", type_="unique")
    # Удаляем колонку username
    op.drop_column("auth", "username")
    # Добавляем колонку login
    op.add_column("auth", sa.Column("login", sa.String(), nullable=False))
    # Создаем уникальное ограничение на login
    op.create_unique_constraint("auth_login_key", "auth", ["login"])


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем уникальное ограничение на login
    op.drop_constraint("auth_login_key", "auth", type_="unique")
    # Удаляем колонку login
    op.drop_column("auth", "login")
    # Добавляем колонку username
    op.add_column("auth", sa.Column("username", sa.String(), nullable=False))
    # Восстанавливаем уникальное ограничение на username
    op.create_unique_constraint("auth_username_key", "auth", ["username"])
