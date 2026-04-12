import copy

from sqlalchemy import func

from src.daos.games_dao import GameDAO
from src.enums import DifficultyNameEnum
from src.schemas.swap import SwapResponse
from src.schemas.game_rules import GameRule
from src.game_logic.game_logic import GameLogic
from src.daos.game_rules_dao import GameRuleDAO
from src.daos.game_fields_dao import GameFieldDAO
from src.daos.difficulties_dao import DifficultyDAO
from src.schemas.games import GameResponse, GameUpdate


class GameService:
    @classmethod
    async def create_game(cls, game_rule: GameRule) -> GameResponse | dict:
        game_difficulty = await DifficultyDAO.find_by_id(id_=game_rule.game_difficulty_id)

        if game_difficulty.difficulty_name != DifficultyNameEnum.CUSTOM.value:
            game_rule.row_count = game_difficulty.row_count_default
            game_rule.col_count = game_difficulty.col_count_default
            game_rule.target_score = game_difficulty.target_score_default
            game_rule.game_items_count = game_difficulty.game_items_count_default
            game_rule.is_one_swap_mode = game_difficulty.is_one_swap_mode_default
            game_rule.is_one_item_mode = game_difficulty.is_one_item_mode_default

        existing_rule = await GameRuleDAO.create(game_rule=game_rule)

        new_field = GameLogic.create_starting_field(row_count=game_rule.row_count,
                                                    col_count=game_rule.col_count,
                                                    items_count=game_rule.game_items_count,
                                                    is_one_swap_mode=game_rule.is_one_swap_mode)
        random_item = GameLogic.get_random_game_item(
            items_count=game_rule.game_items_count) if game_rule.is_one_item_mode else None
        field = await GameFieldDAO.create(field=new_field)
        game = await GameDAO.create(difficulty_id=game_rule.game_difficulty_id, game_rule_id=existing_rule.id,
                                    field_id=field.id, random_game_item=random_item)
        return GameResponse.model_validate(game).model_dump() if game else {}

    @classmethod
    async def update_game(cls, game_id: int, game: GameUpdate) -> GameResponse:
        existing_game = await GameDAO.find_by_id(id_=game_id)
        updated_game = await GameDAO.update(orm_model=existing_game, **game.model_dump(exclude_unset=True))
        return GameResponse.model_validate(updated_game).model_dump()

    @classmethod
    async def get_current_game(cls, game_id: int) -> GameResponse | dict:
        result = await GameDAO.find_by_id(id_=game_id)
        return GameResponse.model_validate(result).model_dump()

    @classmethod
    async def make_swap(cls, game_id: int, row_num: int, col_num: int, swap_type: str) -> list[SwapResponse]:
        game = await GameDAO.find_by_id(id_=game_id)

        GameLogic.validate_game_playing_state(current_score=game.score, target_score=game.game_rules.target_score,
                                              is_over_state=game.is_over, lost_of_time_state=game.lost_of_time)

        field = await GameFieldDAO.find_by_id(id_=game.game_field.id)
        steps = []
        if GameLogic.check_loose(last_action_time=game.last_action_time):
            updated_game = await GameDAO.update(orm_model=game, is_over=True, lost_of_time=True)
        else:
            new_field = GameLogic.swap(field=game.game_field.field['field'], row_num=row_num, col_num=col_num,
                                       swap_type=swap_type)
            game_score = game.score
            is_win = game.is_over
            is_refreshed = False
            is_reverted = False
            counter = 0
            steps.extend([
                {
                    'is_over': is_win,
                    'field': copy.deepcopy(new_field),
                    'score': game_score,
                    'is_refreshed': is_refreshed,
                    'is_reverted': is_reverted,
                    'items_to_destroy': [],
                    'items_to_fall': [],
                    'items_to_spawn': []
                }
            ])
            while True:
                all_matches = GameLogic.get_all_matches(field=new_field, matched_item=game.random_game_item)
                if GameLogic.check_has_matches_from_all_matches(matches=all_matches):
                    marked_field = GameLogic.mark_matches_on_field(field=new_field, matches=all_matches)
                    game_score += GameLogic.calculate_score(marked_field=marked_field)
                    new_field = GameLogic.delete_and_add_new_items_on_field(marked_field=marked_field,
                                                                            items_count=game.game_rules.game_items_count)
                    is_win = GameLogic.check_win(current_score=game_score, target_score=game.game_rules.target_score)
                    steps[counter]['items_to_destroy'] = GameLogic.get_all_item_indexes_to_delete(
                        marked_field=marked_field)
                    steps[counter]['items_to_fall'] = GameLogic.get_all_falls(marked_field=marked_field)
                    steps.extend([
                        {
                            'is_over': is_win,
                            'field': copy.deepcopy(new_field),
                            'score': game_score,
                            'is_refreshed': is_refreshed,
                            'is_reverted': is_reverted,
                            'items_to_destroy': [],
                            'items_to_fall': [],
                            'items_to_spawn': GameLogic.get_all_spawns(marked_field=marked_field)
                        }
                    ])
                    if is_win:
                        counter += 1
                        break
                    counter += 1
                else:
                    if counter == 0 and game.game_rules.is_one_swap_mode:
                        is_reverted = True
                        new_field = game.game_field.field['field']
                        steps.extend([
                            {
                                'is_over': is_win,
                                'field': copy.deepcopy(new_field),
                                'score': game_score,
                                'is_refreshed': is_refreshed,
                                'is_reverted': is_reverted,
                                'items_to_destroy': [],
                                'items_to_fall': [],
                                'items_to_spawn': []
                            }
                        ])
                    break

            if not GameLogic.check_has_potential_moves(field=new_field,
                                                       is_one_swap_mode=game.game_rules.is_one_swap_mode):
                is_refreshed = True
                new_field = GameLogic.create_starting_field(row_count=game.game_rules.row_count,
                                                            col_count=game.game_rules.col_count,
                                                            items_count=game.game_rules.game_items_count,
                                                            is_one_swap_mode=game.game_rules.is_one_swap_mode)
                steps.extend([
                    {
                        'is_over': is_win,
                        'field': copy.deepcopy(new_field),
                        'score': game_score,
                        'is_refreshed': is_refreshed,
                        'is_reverted': is_reverted,
                        'items_to_destroy': [],
                        'items_to_fall': [],
                        'items_to_spawn': [
                            [index_row, index_col] for index_row, row in enumerate(new_field)
                            for index_col, item in enumerate(row)
                        ]
                    }
                ])
            updated_field = await GameFieldDAO.update(orm_model=field, field={'field': new_field})
            updated_game = await GameDAO.update(orm_model=game, score=game_score, is_over=is_win,
                                                last_action_time=func.now())
        return [SwapResponse.model_validate(step).model_dump() for step in steps]

    @classmethod
    async def refresh_game_field(cls, game_id: int, penalty: int) -> SwapResponse:
        game = await GameDAO.find_by_id(id_=game_id)

        GameLogic.validate_game_playing_state(current_score=game.score, target_score=game.game_rules.target_score,
                                              is_over_state=game.is_over, lost_of_time_state=game.lost_of_time)

        field = await GameFieldDAO.find_by_id(id_=game.game_field.id)
        new_field = GameLogic.create_starting_field(
            row_count=game.game_rules.row_count, col_count=game.game_rules.col_count,
            items_count=game.game_rules.game_items_count, is_one_swap_mode=game.game_rules.is_one_swap_mode
        )
        updated_field = await GameFieldDAO.update(orm_model=field, field={'field': new_field})
        updated_game = await GameDAO.update(orm_model=game,
                                            score=GameLogic.apply_score_penalty(current_score=game.score,
                                                                                penalty=penalty),
                                            last_action_time=func.now())
        result = {
            'is_over': False,
            'field': updated_field.field['field'],
            'score': updated_game.score,
            'is_refreshed': True,
            'is_reverted': False,
            'items_to_destroy': [],
            'items_to_fall': [],
            'items_to_spawn': [
                [index_row, index_col] for index_row, row in enumerate(updated_field.field['field'])
                for index_col, item in enumerate(row)
            ]
        }
        return SwapResponse.model_validate(result).model_dump()

    @classmethod
    async def update_losing_games(cls):
        games = await GameDAO.find_all_to_loose()
        for game in games:
            await GameDAO.update_from_id(id_=game.id, is_over=True, lost_of_time=True)
        print(f"Завершено {len(games)} игр из-за неактивности.")

    @classmethod
    async def get_current_game_score(cls, id: int) -> int:
        return await GameDAO.find_score_by_id(id_=id)
