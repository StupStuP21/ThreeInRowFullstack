from fastapi import APIRouter

from src.schemas.swap import SwapResponse
from src.services.games_service import GameService
from src.schemas.games import GameResponse, GameUpdate
from src.exceptions.exceptions import allowed_exceptions_list
from src.exceptions.exceptions_handler import ExceptionCustom

router = APIRouter(prefix='/game', tags=['Игра'])


@router.get("/{game_id}", response_model=GameResponse,
            summary=f"Получение текущей игры и все связанные с ней сущности")
async def get_current_game(game_id: int):
    try:
        return await GameService.get_current_game(game_id=game_id)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))


@router.get("/{game_id}/score", response_model=int, summary="Получение текущего кол-ва очков данной игры")
async def get_current_game_score(game_id: int) -> int:
    try:
        return await GameService.get_current_game_score(id=game_id)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))


@router.post("/{game_id}/swap", response_model=list[SwapResponse], summary="Функция свапа")
async def make_swap(game_id: int, row_num: int, col_num: int, swap_type: str):
    """
    Функция свапа игры. Обновляет поле игры в бд, обновляет кол-во очков, проверяет победа или нет.\n
    Принимает в качестве аргументов: \n

        game_id - id игры;\n
        row_num - номер строки игрового предмета, который спадается (нумерация с 0 - верхняя строка);\n
        col_num - номер столбца игрового предмета, который свапается (нумерация с 0 - левый столбце);\n
        swap_type - тип свапа (string: left|right|up|down)\n

    Возвращает список объектов формата SwapResponse (несколько, в случае того, что свап привёл к цепочке разрушений): \n

        is_over - маркер, игра закончена или нет;\n
        field - обновлённое игровое поле;\n
        score - обновлённое кол-во очков;\n
        is_refreshed - поле было обновлено полностью (для refresh всегда True);\n
        is_reverted - поле было возращено в состояние до свапа, т.к не привело к совпадению 3 в ряд
        (только для режима 'одним свапом', для refresh всегда False)
    """
    try:
        return await GameService.make_swap(game_id=game_id, row_num=row_num, col_num=col_num, swap_type=swap_type)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))


@router.post("/{game_id}/refresh", response_model=SwapResponse, summary="Полное обновление игрового поля")
async def make_refresh_field(game_id: int, score_penalty: int = 5):
    """
    Ручное обновление поля игры с нуля. Обновляет поле игры в бд, обновляет кол-во очков на основе штрафа score_penalty.\n
    Возвращает объект формата SwapResponse: \n

        is_over - маркер, игра закончена или нет;\n
        field - обновлённое игровое поле;\n
        score - обновлённое кол-во очков;\n
        is_refreshed - поле было обновлено полностью (для refresh всегда True);\n
        is_reverted - поле было возращено в состояние до свапа, т.к не привело к совпадению 3 в ряд
        (только для режима 'одним свапом', для refresh всегда False)
    """
    try:
        return await GameService.refresh_game_field(game_id=game_id, penalty=score_penalty)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))


@router.patch("/{game_id}", response_model=GameResponse, summary="Обновление любого поля объекта игры в бд")
async def update_fields(game_id: int, game_update: GameUpdate):
    try:
        return await GameService.update_game(game_id=game_id, game=game_update)
    except allowed_exceptions_list as exception:
        raise ExceptionCustom(status_code=404, detail=str(exception))
