"""add_difficulties_into_db

Revision ID: c89dc93fd5e9
Revises: 97e6e1978b32
Create Date: 2025-12-19 20:03:28.473306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c89dc93fd5e9'
down_revision: Union[str, Sequence[str], None] = '97e6e1978b32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    table = sa.table(
        'difficulties',
        sa.Column('difficulty_name', sa.String(), nullable=False),
        sa.Column('row_count_default', sa.Integer(), nullable=True),
        sa.Column('col_count_default', sa.Integer(), nullable=True),
        sa.Column('target_score_default', sa.Integer(), nullable=True),
        sa.Column('is_one_swap_mode_default', sa.Boolean(), nullable=True),
        sa.Column('is_one_item_mode_default', sa.Boolean(), nullable=True),
    )
    op.bulk_insert(
        table,
        [
            {"difficulty_name": "Простой", "row_count_default": 12, "col_count_default": 12, "target_score_default": 40,
             "is_one_swap_mode_default": False, "is_one_item_mode_default": False},
            {"difficulty_name": "Средний", "row_count_default": 8, "col_count_default": 8, "target_score_default": 50,
             "is_one_swap_mode_default": True, "is_one_item_mode_default": False},
            {"difficulty_name": "Сложный", "row_count_default": 8, "col_count_default": 8, "target_score_default": 25,
             "is_one_swap_mode_default": True, "is_one_item_mode_default": True},
            {"difficulty_name": "Кастомный", "row_count_default": None, "col_count_default": None,
             "target_score_default": None, "is_one_swap_mode_default": None, "is_one_item_mode_default": None},
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DELETE FROM difficulties WHERE difficulty_name IN ('Простой', 'Средний', 'Сложный', 'Кастомный');
        """
    )
