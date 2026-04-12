from src.daos.base_dao import BaseDAO
from src.db.models.difficulties import Difficulty


class DifficultyDAO(BaseDAO):
    model = Difficulty

    @classmethod
    async def find_custom_difficulty(cls, name: str = 'Кастомный') -> Difficulty:
        return await cls.find_one_existing_by_params(difficulty_name=name)
