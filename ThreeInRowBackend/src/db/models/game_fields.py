from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class GameField(Base):
    __tablename__ = "game_fields"
    field: Mapped[dict] = mapped_column(JSON, nullable=False)

    game: Mapped["Game"] = relationship(back_populates="game_field", lazy='subquery')
