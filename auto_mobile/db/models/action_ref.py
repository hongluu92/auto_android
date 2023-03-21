from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Identity, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class ActionRef(Base):
    __tablename__ = "action_refs"

    child_id = Column(Integer,ForeignKey("actions.id"),primary_key=True, index=True)
    parrent_id = Column(Integer,ForeignKey("actions.id"), primary_key=True, index=True , nullable= True)
    loop = Column(Integer, default= 0)
    loop_delay = Column(Integer, default= 1000)
    # child  = relationship("Action", back_populates="parrents", lazy= "select")
    # parrent  = relationship("Action", back_populates="childs", lazy='childs' )



