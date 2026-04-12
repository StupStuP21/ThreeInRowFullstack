import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from typing_extensions import override

from src.daos.base_dao import BaseDAO
from src.db.models.games import Game
from src.db.database import SessionLocal
from src.exceptions.exceptions import ObjectNotFoundException


class GameDAO(BaseDAO):
    model = Game

    @classmethod
    async def create(cls, difficulty_id: int, game_rule_id: int, field_id: int,
                     random_game_item: str | None = None) -> Game | None:
        return await cls.create_from_model(
            orm_model=Game(
                difficulty_id=difficulty_id, game_rule_id=game_rule_id, field_id=field_id,
                random_game_item=random_game_item
            )
        )

    @classmethod
    @override
    async def find_by_id(cls, id_: int = None) -> Game:
        async with SessionLocal() as db:
            result = await db.scalars(
                select(cls.model).options(
                    joinedload(cls.model.game_field),
                    joinedload(cls.model.difficulty),
                    joinedload(cls.model.game_rules)
                ).where(cls.model.id == id_)
            )
            result = result.first()
        if result is None:
            raise ObjectNotFoundException(model_name=cls.model.__name__, id_=id_)
        return result

    @classmethod
    async def find_best_games(cls, difficulty_id: int, limit_count: int) -> list[tuple]:
        async with SessionLocal() as db:
            result = await db.scalars(
                select(cls.model).options(
                    joinedload(cls.model.game_field),
                    joinedload(cls.model.difficulty),
                    joinedload(cls.model.game_rules)
                ).where(
                    cls.model.difficulty_id == difficulty_id,
                    cls.model.is_over == True,
                    cls.model.lost_of_time == False
                ).order_by(
                    cls.model.last_action_time - cls.model.start_time
                ).limit(limit_count)
            )
        return result.all()

    @classmethod
    async def find_all_to_loose(cls) -> list[Game]:
        async with SessionLocal() as db:
            result = await db.scalars(
                select(cls.model).where(cls.model.is_over == False,
                                        cls.model.last_action_time < func.now() - datetime.timedelta(hours=2))
            )
        return result.all()

    @classmethod
    async def find_score_by_id(cls, id_: int) -> int:
        async with SessionLocal() as db:
            result = await db.scalars(
                select(cls.model.score).where(cls.model.id == id_)
            )
            result = result.first()
            if result is None:
                raise ObjectNotFoundException(model_name=cls.model.__name__, id_=id_)
        return result
