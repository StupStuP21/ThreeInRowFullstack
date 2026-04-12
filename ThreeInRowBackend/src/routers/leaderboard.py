from fastapi import APIRouter

from src.services.leaderboard_service import LeaderboardService
from src.schemas.leaderboard import LeaderboardResponse
from src.exceptions.exceptions import allowed_exceptions_list
from src.exceptions.exceptions_handler import ExceptionCustom

router = APIRouter(prefix='/leaderboard', tags=['Таблица лидеров'])


@router.get("/{difficulty_id}", response_model=list[LeaderboardResponse], summary="Получение лучших N-игр по сложности")
async def get_leaderboard(difficulty_id: int, limit: int = 10):
    try:
        return await LeaderboardService.get_best_games_by_difficulty(difficulty_id=difficulty_id, limit_count=limit)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))
