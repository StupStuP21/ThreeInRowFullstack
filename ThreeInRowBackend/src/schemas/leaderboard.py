import datetime

from pydantic import BaseModel

from src.enums import DifficultyNameEnum


class LeaderboardResponse(BaseModel):
    difficulty_name: DifficultyNameEnum
    difficulty_id: int
    game_id: int
    score: int
    game_time_seconds: int