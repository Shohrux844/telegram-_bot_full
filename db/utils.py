from sqlalchemy import Column, DateTime, Integer, func, text
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.orm import declared_attr

from db import db, Base

db.init() # conecshin qilish


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def create(cls, **kwargs):
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, id_):
        query = select(cls).where(cls.id == id_)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        await db.execute(query)
        await cls.commit()
        return True

    @classmethod
    async def get_all(cls, order_fields: list[str] = None):
        query = select(cls)
        if order_fields:
            query = query.order_by(*order_fields)
        objects = await db.execute(query)
        result = []
        for i in objects.all():
            result.append(i[0])
        return result


tz = "TIMEZONE('Asia/Tashkent', NOW())"


class CreatedModel(Base, AbstractClass):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=text(tz))
    updated_at = Column(DateTime(timezone=True), server_default=text(tz), onupdate=func.now())
