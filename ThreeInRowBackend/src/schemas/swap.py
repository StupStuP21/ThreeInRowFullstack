from pydantic import BaseModel


class SwapResponse(BaseModel):
    is_over: bool
    field: list[list[str]]
    items_to_destroy: list[list[int]]
    items_to_fall: list[list[int]]
    items_to_spawn: list[list[int]]
    score: int
    is_refreshed: bool
    is_reverted: bool