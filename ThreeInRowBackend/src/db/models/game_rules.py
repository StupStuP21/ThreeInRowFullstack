from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, UniqueConstraint

from src.db.models.base import Base


class GameRule(Base):
    __tablename__ = "game_rules"
    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    col_count: Mapped[int] = mapped_column(Integer, nullable=False)
    target_score: Mapped[int] = mapped_column(Integer, nullable=False)
    game_items_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_one_swap_mode: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_one_item_mode: Mapped[bool] = mapped_column(Boolean, nullable=False)
    games: Mapped[list["Game"]] = relationship(back_populates="game_rules", lazy='subquery')
    __table_args__ = (
        UniqueConstraint('row_count', 'col_count', 'target_score', 'is_one_swap_mode', 'is_one_item_mode',
                         'game_items_count'),
    )
