from typing import Any, Tuple

from sqlalchemy import Table, Column, Integer, Identity
from sqlalchemy.orm import as_declarative

from auto_mobile.db.meta import meta


@as_declarative(metadata=meta)
class Base:
    """
    Base for all models.
    It has some type definitions to
    enhance autocompletion.
    """
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True, index=True)
    __tablename__: str
    __table__: Table
    __table_args__: Tuple[Any, ...]