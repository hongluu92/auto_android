from typing import Any, List
import base64
from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
from ppadb.client import Client as AdbClient
from ppadb.device import Device
import cv2
import numpy as np
from auto_mobile.db import dependencies
from auto_mobile.db.models import Action
from auto_mobile.db.repositoies.script_action_repo import ScriptActionRepository
from sqlalchemy.orm import Session
from auto_mobile.errors.http_res_err import HttpResException
from auto_mobile.web.const import ActionType

from auto_mobile.web.schema.action import ScriptActionVO
import time
from loguru import logger
import os
router = APIRouter()
BASE_IMG_URL = "auto_mobile/static/imgs/"
CURRENT_IMG = "current_img.png"
def getDevices() -> List[Device]:
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if (len(devices) < 0):
        print("0 device")
        return 0

    return devices

def getDevice() -> List[Device]:
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if (len(devices) < 0):
        print("0 device")
        return 0

    return devices[0]

@router.get("/", response_model= List[ScriptActionVO], status_code=201)
def get_action(
    script_id:int ,
    db :Session = Depends(dependencies.get_db_session) ,
    page_size: int = 100,
    page: int = 0,
    
) -> Any:
    """
    Get Script action
    """
    if script_id == 0:
        raise HttpResException("Missing script_id", "missing_script_id")
    scriptActionRepo = ScriptActionRepository()
    results =  scriptActionRepo.get_multi_by_script_id(db,script_id,page,page_size)
    for result in results:
        yield ScriptActionVO.from_orm(result)
    


@router.post("/", response_model= ScriptActionVO, status_code=201)
def create_action(
    *,
    db :Session = Depends(dependencies.get_db_session) ,
    actionVO: ScriptActionVO
) -> Any:
    """
    Create Script action
    """
    # if actionVO.action_type == ActionType.TAP_BY_IMAGE or actionVO.action_type == ActionType.CHECK_BY_IMAGE:
   
    scriptActionRepo = ScriptActionRepository()
    scripActionDb = scriptActionRepo.create(db = db,obj_in = actionVO)
    device = getDevice()
    img = device.screencap()
    nparr = np.asarray(bytearray(img), dtype=np.uint8)
    image = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
    folder_path = BASE_IMG_URL+ "{}/{}".format(scripActionDb.script.game,scripActionDb.script_id)
    isExist = os.path.exists(folder_path)
    if not isExist:
        os.makedirs(folder_path)
    image_path ="{}/{}/{}.png".format(scripActionDb.script.game,scripActionDb.script_id,scripActionDb.id)
    cv2.imwrite(BASE_IMG_URL+ image_path,image)
    actionVO.img = image_path
    actionVO.id = scripActionDb.id
    return scriptActionRepo.update(db = db, db_obj=scripActionDb, obj_in = actionVO)

@router.put("/", response_model= ScriptActionVO, status_code=201)
def update_action(
    *,
    db :Session = Depends(dependencies.get_db_session) ,
    actionVO: ScriptActionVO
) -> Any:
    """
    Create Script action
    
    """
    device = getDevice()
    img = device.screencap()
    nparr = np.asarray(bytearray(img), dtype=np.uint8)
    image = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        #img_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
       
    scriptActionRepo = ScriptActionRepository()
    scripActionDb = scriptActionRepo.get(db, actionVO.id)
    image_path ="{}/{}/{}.png".format(scripActionDb.script.game,scripActionDb.script_id,scripActionDb.id)
    cv2.imwrite(BASE_IMG_URL+ image_path,image)
    return scriptActionRepo.update(db = db, db_obj=scripActionDb, obj_in = actionVO)

@router.delete("/{id}", response_model= str, status_code=201)
def delete_action(
    id: int, 
    db :Session = Depends(dependencies.get_db_session) ,  
) -> Any:
    """
    Create Script action
    """
    scriptActionRepo = ScriptActionRepository()
    scriptActionRepo.remove(db = db,id= id)

    return "delete OK"


@router.get("/{id}", response_model= ScriptActionVO, status_code=201)
def delete_action_by(
    id: int, 
    db :Session = Depends(dependencies.get_db_session) ,  
) -> Any:
    """
    Delete Script action
    """
    scriptActionRepo = ScriptActionRepository()
    return scriptActionRepo.get(db = db,id= id)

@router.post("/reload-current-img", response_model= str, status_code=201)
def reloadCurrentImg() -> Any:
    """
    reloadCurrentImg
    """
    # return "OK"
    try:
        device = getDevice()
        img = device.screencap()
        nparr = np.asarray(bytearray(img), dtype=np.uint8)
        img_np = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        #img_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(BASE_IMG_URL+CURRENT_IMG,img_np)
    except Exception as e:
        raise HttpResException("Không tìm thấy thiết bị", "missing_device", e.args)
    return "OK"

@router.post("/run", response_model= str, status_code=201)
def run(actionVO: ScriptActionVO) -> Any:
    """
    run
    """
    # return "OK"
    try:
        device :Device = getDevice()
        img = device.screencap()
        nparr = np.asarray(bytearray(img), dtype=np.uint8)
        img_np = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        #img_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(BASE_IMG_URL+CURRENT_IMG,img_np)
        if (actionVO.action_type == ActionType.TAP):
            x, y = actionVO.getRealTapPostion()
            device.input_tap(x, y)
        if (actionVO.action_type == ActionType.TAP_BY_IMAGE):
            compare_img_path = CURRENT_IMG
            if actionVO.img:
                compare_img_path =  actionVO.img
            compare_img = cv2.imread(BASE_IMG_URL + compare_img_path, 0)
            img = cv2.imread(BASE_IMG_URL + CURRENT_IMG, 0)
            x, y = actionVO.getRealImageComparePostion(img, compare_img)
            device.input_tap(x, y)
        time.sleep(0.5)
    except Exception as e:
        raise HttpResException("Không tìm thấy thiết bị", "missing_device", e.args)
    return "OK"