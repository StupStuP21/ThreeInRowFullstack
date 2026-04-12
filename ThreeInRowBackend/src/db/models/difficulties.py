from src.db.models.base import Base
from src.enums import DifficultyNameEnum
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Difficulty(Base):
    __tablename__ = "difficulties"
    difficulty_name: Mapped[DifficultyNameEnum] = mapped_column(String, nullable=False, unique=True)
    row_count_default: Mapped[int] = mapped_column(Integer, nullable=True)
    col_count_default: Mapped[int] = mapped_column(Integer, nullable=True)
    target_score_default: Mapped[int] = mapped_column(Integer, nullable=True)
    game_items_count_default: Mapped[int] = mapped_column(Integer, nullable=True)
    is_one_swap_mode_default: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_one_item_mode_default: Mapped[bool] = mapped_column(Boolean, nullable=True)

    games: Mapped[list["Game"]] = relationship(back_populates="difficulty", lazy='subquery')
