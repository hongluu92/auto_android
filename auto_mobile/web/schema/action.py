from typing import Optional
from pydantic import BaseModel, Field
from typing import Any, List

from auto_mobile.web.schema.script_vo import ScriptVO
import random
import cv2
import numpy as np
BASE_IMG_URL = "auto_mobile/static/imgs/"

class ActionVOCreated(BaseModel):
    id : int = None
    # tap, key_event, compare_image, swipe, check
    action_type : str = "tap"
    
    event_type : str = None
    tap_position : str = None
    swipe_position : str = None #Column(String , comment : "swipe from (x_start,y_start) to (x_end y_end): x_start y_start x_end y_end")
    img_compare_bb : str = None #Column(String, comment : "Boudingbox image need to compare: x_start y_start x_end y_end")
    image_compare_threshhold:int = 0.8
    key_event : str  = None #Column(String)
    img : str = None #Column(String, comment : "Current Image")
    loop : int = 1 #Column(Integer, default: 0)
    loop_delay : int  = 1000 #Column(Integer, default: 1000)
    description : str = None #Column(String)
    order_index : int = 0
    parrent_id : int = None
    new_thread : bool = False
    scale: float = 0
    

    class Config:
        orm_mode = True

    def getRealTapPostion(self):
        tap_position = self.tap_position.split(" ")
        return int(tap_position[0])/self.scale + random.randint(0, 9), int(tap_position[1])/self.scale  + random.randint(0, 9)

    def getRealScreenPostion(self):
        tap_position = self.tap_position.split(" ")
        return int(tap_position[0])/self.scale + random.randint(0, 9), int(tap_position[1])/self.scale  + random.randint(0, 9)
    
    def __getRealImageComparePostion(self):
        tap_position = self.img_compare_bb.split(" ")
        for i in range( len(tap_position)):
            tap_position[i] = int(tap_position[i])
        return int(tap_position[0]/self.scale ), int(tap_position[1]/self.scale) , int(tap_position[2]/self.scale), int(tap_position[3]/self.scale)
    
    def getRealImageComparePostion(self, current_img, compare_image):
        x, y, h, w = self.__getRealImageComparePostion()
        compare_image = compare_image[y:y+h, x:x+w]
        res = cv2.matchTemplate(current_img, compare_image, cv2.TM_CCOEFF_NORMED)
        THRESHOLD = 0.9
        loc = np.where(res >= THRESHOLD)
        index1, index2 = 0,0
        # #Draw boudning box
        w, h = compare_image.shape[1], compare_image.shape[0]
        for y, x in zip(loc[0], loc[1]):
            index1, index2 = x + w/2, y + h/2
            break
          
        return index1, index2

    def getImgPath(self):
        return BASE_IMG_URL.format("{}/{}.png", self.script_id, self.id)

class ActionVO(ActionVOCreated):
    childs: List = []

class ScriptActionVO(BaseModel):
    script_id: int
    action_id:int
    action: ActionVO 
    loop: int = 1
    loop_delay: int  = 1000