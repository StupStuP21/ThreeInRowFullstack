from sqlalchemy import select, update
from src.db.database import SessionLocal
from src.exceptions.exceptions import ObjectNotFoundException


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with SessionLocal() as db:
            return await db.scalars(select(cls.model).filter_by(**filter_by))

    @classmethod
    async def find_by_id(cls, id_: int = None):
        async with SessionLocal() as db:
            result = await db.scalars(select(cls.model).filter_by(id=id_))
            result = result.first()
            if result is None:
                raise ObjectNotFoundException(model_name=cls.model.__name__, id_=id_)
            return result

    @classmethod
    async def find_one_existing_by_params(cls, **filter_by):
        async with SessionLocal() as db:
            result = await db.scalars(select(cls.model).filter_by(**filter_by))
            return result.first()

    @classmethod
    async def update_from_id(cls, id_: int, **params):
        async with SessionLocal() as db:
            await db.execute(update(cls.model).where(cls.model.id == id_).values(**params))
            await db.commit()

    @classmethod
    async def update(cls, orm_model, **params):
        if type(orm_model) != cls.model:
            raise TypeError(f"Function should have a orm_model parameter with {cls.model} type")
        async with SessionLocal() as db:
            for param_name, param_value in params.items():
                if hasattr(orm_model, param_name) and param_name != 'id':
                    setattr(orm_model, param_name, param_value)
            db.add(orm_model)
            await db.commit()
            await db.refresh(orm_model)
            return orm_model

    @classmethod
    async def create_from_model(cls, orm_model):
        if type(orm_model) != cls.model:
            raise TypeError(f"Function should have a orm_model parameter with {cls.model} type")
        async with SessionLocal() as db:
            try:
                db.add(orm_model)
                await db.commit()
                await db.refresh(orm_model)
                return orm_model
            except:
                return None
