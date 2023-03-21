from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Identity, ForeignKey
from sqlalchemy.orm import relationship, backref
from .base import Base

if TYPE_CHECKING:
    from .action import Action

class ScriptAction(Base):
    __tablename__ = "script_actions"

    script_id = Column(Integer,ForeignKey("scripts.id"), primary_key=True, index=True)
    action_id = Column(Integer,ForeignKey("actions.id"), primary_key=True, index=True)
    loop = Column(Integer, default= 0)
    loop_delay = Column(Integer, default= 1)
    action  = relationship("Action", backref=backref("action", remote_side='Action.id'), lazy= "joined")
    script = relationship("Script", back_populates="scriptActions", lazy='joined' )



