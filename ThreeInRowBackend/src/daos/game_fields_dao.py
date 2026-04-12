from src.daos.base_dao import BaseDAO
from src.db.models.game_fields import GameField

class GameFieldDAO(BaseDAO):
    model = GameField

    @classmethod
    async def create(cls, field: list[list[str]]) -> GameField:
        return await cls.create_from_model(orm_model=GameField(field={'field': field}))