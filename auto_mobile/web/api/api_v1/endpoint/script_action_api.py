from typing import Any, List

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
from ppadb.client import Client as AdbClient
from ppadb.device import Device
import cv2
import numpy as np
from auto_mobile.db import dependencies
from auto_mobile.db.models import ScriptAction
from auto_mobile.db.repositoies.script_action_repo import ScriptActionRepository
from sqlalchemy.orm import Session
from auto_mobile.errors.http_res_err import HttpResException

from auto_mobile.web.schema.script_action import ScriptActionVO

from loguru import logger
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
def get_scripts(
    script_id:int ,
    db :Session = Depends(dependencies.get_db_session) ,
    page_size: int = 100,
    page: int = 1,
    
) -> Any:
    """
    Get Scripts
    """
    if script_id == 0:
        raise HttpResException("Missing script_id", "missing_script_id")
    scriptRepo = ScriptActionRepository()
    results =  scriptRepo.get_multi_by_script_id(db,script_id,page,page_size)
    for result in results:
        yield ScriptActionVO.from_orm(result)
    


@router.post("/", response_model= ScriptActionVO, status_code=201)
def create_scripts(
    *,
    db :Session = Depends(dependencies.get_db_session) ,
    scriptVO: ScriptActionVO
) -> Any:
    """
    Create Scripts
    """
    scriptRepo = ScriptActionRepository()
    return scriptRepo.create(db = db,obj_in = scriptVO)

@router.put("/", response_model= ScriptActionVO, status_code=201)
def update_scripts(
    *,
    db :Session = Depends(dependencies.get_db_session) ,
    scriptVO: ScriptActionVO
) -> Any:
    """
    Create Scripts
    """
    scriptRepo = ScriptActionRepository()
    script_db = scriptRepo.get(db, scriptVO.id)
    return scriptRepo.update(db = db, db_obj=script_db, obj_in = scriptVO)

@router.delete("/{id}", response_model= str, status_code=201)
def delete_scripts(
    id: int, 
    db :Session = Depends(dependencies.get_db_session) ,  
) -> Any:
    """
    Create Scripts
    """
    scriptRepo = ScriptActionRepository()
    scriptRepo.remove(db = db,id= id)

    return "delete OK"


@router.get("/{id}", response_model= ScriptActionVO, status_code=201)
def delete_scripts(
    id: int, 
    db :Session = Depends(dependencies.get_db_session) ,  
) -> Any:
    """
    Create Scripts
    """
    scriptRepo = ScriptActionRepository()
    return scriptRepo.get(db = db,id= id)

@router.post("/reload-current-img", response_model= str, status_code=201)
def reloadCurrentImg() -> Any:
    """
    Create Scripts
    """
    try:
        device = getDevice()
        img = device.screencap()
        nparr = np.asarray(bytearray(img), dtype=np.uint8)
        img_np = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
        #img_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(BASE_IMG_URL+CURRENT_IMG,img_np)
    except:
        raise HttpResException("Không tìm thấy thiết bị", "missing_device")
    return "OK"