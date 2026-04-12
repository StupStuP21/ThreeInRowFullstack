from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.db.models.game_rules import GameRule as GameRuleORM


class GameRuleResponse(BaseModel):
    row_count: int
    col_count: int
    target_score: int
    game_items_count: int
    is_one_swap_mode: bool
    is_one_item_mode: bool
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class GameRule(BaseModel):
    row_count: int
    col_count: int
    target_score: int
    game_items_count: int
    is_one_swap_mode: bool
    is_one_item_mode: bool
    game_difficulty_id: int

    def cast_to_sqlalchemy(self) -> GameRuleORM:
        return GameRuleORM(
            row_count=self.row_count,
            col_count=self.col_count,
            target_score=self.target_score,
            game_items_count=self.game_items_count,
            is_one_swap_mode=self.is_one_swap_mode,
            is_one_item_mode=self.is_one_item_mode
        )
