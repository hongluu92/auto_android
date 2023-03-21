from typing import TYPE_CHECKING, List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Identity, Float
from sqlalchemy.orm import relationship, backref
from .base import Base
from .action_ref import ActionRef

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer,Identity(start=1, cycle=True), primary_key=True, index=True, autoincrement=True)
    # step_action; break_condition
    action_type = Column(String)
    # tap, key_event, compare_image, swipe, check
    event_type = Column(String)

    tap_position = Column(String, comment= "x y")
    swipe_position = Column(String , comment = "swipe from (x_start,y_start) to (x_end y_end): x_start y_start x_end y_end")
    img_compare_bb = Column(String, comment = "Boudingbox image need to compare: x_start y_start x_end y_end")
    is_click_all_image = Column(Boolean, default= False)
    key_event = Column(String)
    img = Column(String, comment = "Current Image")
    loop = Column(Integer, default= 0)
    loop_delay = Column(Integer, default= 1000)
    order_index = Column(Integer)
    scale = Column(Float)
    image_compare_threshhold= Column(Float)
    new_thread = Column(Boolean, default= False)
    description = Column(String)
    
    # scriptActions  = relationship("ScriptAction", back_populates="action")
    childs   =  relationship('ActionRef',
                                 secondary='action_refs',
                                 primaryjoin=id==ActionRef.parrent_id,
                                 secondaryjoin=id==ActionRef.child_id,
                                 backref='childs', lazy="joined", join_depth= 1)

      