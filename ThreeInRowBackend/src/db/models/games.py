from datetime import datetime

from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base
from src.db.models.game_fields import GameField
from src.db.models.difficulties import Difficulty
from src.db.models.game_rules import GameRule


class Game(Base):
    __tablename__ = "games"
    difficulty_id: Mapped[int] = mapped_column(Integer,
                                               ForeignKey("difficulties.id", onupdate="CASCADE", ondelete="CASCADE"))
    game_rule_id: Mapped[int] = mapped_column(Integer,
                                              ForeignKey("game_rules.id", onupdate="CASCADE", ondelete="CASCADE"))
    field_id: Mapped[int] = mapped_column(Integer,
                                          ForeignKey("game_fields.id", onupdate="CASCADE", ondelete="CASCADE"))
    random_game_item: Mapped[str] = mapped_column(String, nullable=True)
    score: Mapped[int] = mapped_column(Integer, default=0)
    start_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_action_time: Mapped[datetime] = mapped_column(DateTime, nullable=True, server_default=func.now())
    is_over: Mapped[bool] = mapped_column(Boolean, default=False)
    lost_of_time: Mapped[bool] = mapped_column(Boolean, default=False)

    game_field: Mapped["GameField"] = relationship(back_populates="game", lazy='subquery')
    difficulty: Mapped["Difficulty"] = relationship(back_populates="games", lazy='subquery')
    game_rules: Mapped["GameRule"] = relationship(back_populates="games", lazy='subquery')