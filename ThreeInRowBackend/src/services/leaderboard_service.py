from src.daos.games_dao import GameDAO
from src.schemas.leaderboard import LeaderboardResponse


class LeaderboardService:
    @classmethod
    async def get_best_games_by_difficulty(cls, difficulty_id: int, limit_count=10) -> list[LeaderboardResponse]:
        games = await GameDAO.find_best_games(difficulty_id=difficulty_id, limit_count=limit_count)
        return [LeaderboardResponse.model_validate({
            'difficulty_name': game.difficulty.difficulty_name,
            'difficulty_id': game.difficulty_id,
            'game_id': game.id,
            'score': game.score,
            'game_time_seconds': (game.last_action_time - game.start_time).seconds
        }).model_dump() for game in games]
