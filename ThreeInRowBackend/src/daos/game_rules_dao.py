from src.daos.base_dao import BaseDAO
from src.schemas.game_rules import GameRule
from src.db.models.game_rules import GameRule as GameRuleORM


class GameRuleDAO(BaseDAO):
    model = GameRuleORM

    @classmethod
    async def get_existing_rule(cls, row_count: int, col_count: int, target_score: int, game_items_count: int,
                                is_one_swap_mode: bool, is_one_item_mode: bool) -> GameRuleORM:
        return await cls.find_one_existing_by_params(
            row_count=row_count,
            col_count=col_count,
            target_score=target_score,
            game_items_count=game_items_count,
            is_one_swap_mode=is_one_swap_mode,
            is_one_item_mode=is_one_item_mode
        )

    @classmethod
    async def create(cls, game_rule: GameRule) -> GameRuleORM:
        game_rule_orm = game_rule.cast_to_sqlalchemy()
        existing_rule = await cls.get_existing_rule(row_count=game_rule_orm.row_count,
                                                    col_count=game_rule_orm.col_count,
                                                    target_score=game_rule_orm.target_score,
                                                    game_items_count=game_rule_orm.game_items_count,
                                                    is_one_swap_mode=game_rule_orm.is_one_swap_mode,
                                                    is_one_item_mode=game_rule_orm.is_one_item_mode)
        if not existing_rule:
            existing_rule = await cls.create_from_model(orm_model=game_rule_orm)
        return existing_rule
