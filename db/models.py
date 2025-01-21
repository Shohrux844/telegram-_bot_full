from sqlalchemy.orm import Mapped
from sqlalchemy.testing.suite.test_reflection import metadata

from db import Base
from db.utils import CreatedModel


class Category(CreatedModel):
    __tablename__ = 'categories'
    name: Mapped[str]


metadata = Base.metadata
