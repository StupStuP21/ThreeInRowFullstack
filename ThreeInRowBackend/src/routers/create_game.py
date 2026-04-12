from fastapi import APIRouter

from src.schemas.game_rules import GameRule
from src.schemas.games import GameResponse
from src.services.games_service import GameService
from src.exceptions.exceptions import allowed_exceptions_list
from src.exceptions.exceptions_handler import ExceptionCustom

router = APIRouter(prefix='/create_game', tags=['Создание игры'])


@router.post("/create", response_model=GameResponse, summary="Создание игры")
async def create_new_game(game_rule: GameRule):
    """
    Функция для создания игры. В игре 4 сложности, если была задана не кастомная сложность,
     то в бд запишется игра с соответствующей сложностью и соответствующей это сложностью дефолтными параметрами игрового правила, независимо от указанных
    """
    try:
        return await GameService.create_game(game_rule=game_rule)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))
