from src.daos.difficulties_dao import DifficultyDAO
from src.schemas.difficulties import DifficultyResponse

class DifficultyService:
    @classmethod
    async def get_all_difficulties(cls, difficulty_name: str | None = None) -> list[DifficultyResponse]:
        if difficulty_name:
            result = await DifficultyDAO.find_all(difficulty_name=difficulty_name)
        else:
            result = await DifficultyDAO.find_all()
        return [DifficultyResponse.model_validate(difficulty).model_dump() for difficulty in result]

    @classmethod
    async def get_difficulty_by_id(cls, difficulty_id: int) -> DifficultyResponse:
        result = await DifficultyDAO.find_by_id(id_=difficulty_id)
        return DifficultyResponse.model_validate(result).model_dump()