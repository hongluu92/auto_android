from typing import Optional
from pydantic import BaseModel, Field
from typing import Any, List

from auto_mobile.web.schema.script_vo import ScriptVO

class ScriptActionVO(BaseModel):
    id : int = None
    # step_action; break_condition
    action_type : str
    # tap, key_event, compare_image, swipe, check
    event_type : str

    tap_position : str
    swipe_position : str #Column(String , comment : "swipe from (x_start,y_start) to (x_end y_end): x_start y_start x_end y_end")
    img_compare_bb : str #Column(String, comment : "Boudingbox image need to compare: x_start y_start x_end y_end")
    key_event : str #Column(String)
    img : str #Column(String, comment : "Current Image")
    loop : int #Column(Integer, default: 0)
    loop_delay : int #Column(Integer, default: 1000)
    description : str #Column(String)
    script_id : int #Column(Integer, ForeignKey("scripts.id"))
    
    class Config:
        orm_mode = True