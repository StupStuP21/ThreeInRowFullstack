from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.enums import DifficultyNameEnum


class DifficultyResponse(BaseModel):
    difficulty_name: DifficultyNameEnum
    row_count_default: int | None
    col_count_default: int | None
    target_score_default: int | None
    game_items_count_default: int | None
    is_one_swap_mode_default: bool | None
    is_one_item_mode_default: bool | None
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
