from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Identity
from sqlalchemy.orm import relationship
from .base import Base

class ScriptAction(Base):
    __tablename__ = "script_actions"

    id = Column(Integer,Identity(start=1, cycle=True), primary_key=True, index=True, autoincrement=True)
    # step_action; break_condition
    action_type = Column(String)
    # tap, key_event, compare_image, swipe, check
    event_type = Column(String)

    tap_position = Column(String, comment= "x y")
    swipe_position = Column(String , comment = "swipe from (x_start,y_start) to (x_end y_end): x_start y_start x_end y_end")
    img_compare_bb = Column(String, comment = "Boudingbox image need to compare: x_start y_start x_end y_end")
    key_event = Column(String)
    img = Column(String, comment = "Current Image")
    loop = Column(Integer, default= 0)
    loop_delay = Column(Integer, default= 1000)
    description = Column(String)
    script_id = Column(Integer, ForeignKey("scripts.id"))
    script  = relationship("Script", back_populates="actions")  