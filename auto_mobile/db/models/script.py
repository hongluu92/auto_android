from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import relationship
from .base import Base

if TYPE_CHECKING:
    from .script_action import ScriptAction

class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer,Identity(start=1, cycle=True), primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    game = Column(String)
    loop = Column(Integer, default= 0)
    loop_delay = Column(Integer, default= 1)
    actions  = relationship("ScriptAction", back_populates="script")


