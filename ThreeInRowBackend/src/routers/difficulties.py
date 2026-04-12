from fastapi import APIRouter

from src.services.difficulties_service import DifficultyService
from src.schemas.difficulties import DifficultyResponse
from src.exceptions.exceptions import allowed_exceptions_list
from src.exceptions.exceptions_handler import ExceptionCustom

router = APIRouter(prefix='/difficulties', tags=['Уровни сложности'])


@router.get("/", response_model=list[DifficultyResponse], summary="Получение списка объектов всех сложностей игры")
async def get_difficulties(name: str | None = None):
    """
    Получение списка всех сложностей игры с фильтром name, если необходимо
    """
    try:
        return await DifficultyService.get_all_difficulties(difficulty_name=name)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))


@router.get("/{difficulty_id}", response_model=DifficultyResponse, summary="Получение объекта сложности по его id")
async def get_difficulty_by_id(difficulty_id: int):
    try:
        return await DifficultyService.get_difficulty_by_id(difficulty_id=difficulty_id)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))
