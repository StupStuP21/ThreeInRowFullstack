from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, field_serializer
from src.schemas.game_fields import GameFieldResponse
from src.schemas.difficulties import DifficultyResponse
from src.schemas.game_rules import GameRuleResponse


class GameResponse(BaseModel):
    id: int
    difficulty_id: int
    game_rule_id: int
    field_id: int
    random_game_item: Optional[str] = None
    score: int
    start_time: datetime
    last_action_time: Optional[datetime] = None
    is_over: bool
    lost_of_time: bool
    game_field: Optional[GameFieldResponse] = None
    difficulty: Optional[DifficultyResponse] = None
    game_rules: Optional[GameRuleResponse] = None
    model_config = ConfigDict(from_attributes=True)

    @field_serializer('start_time', 'last_action_time')
    def serialize_dt(self, dt: Optional[datetime]) -> Optional[str]:
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()

class GameUpdate(BaseModel):
    difficulty_id: Optional[int] = None
    game_rule_id: Optional[int] = None
    field_id: Optional[int] = None
    random_game_item: Optional[str] = None
    score: Optional[int] = None
    start_time: Optional[datetime] = None
    last_action_time: Optional[datetime] = None
    is_over: Optional[bool] = None
    lost_of_time: Optional[bool] = None