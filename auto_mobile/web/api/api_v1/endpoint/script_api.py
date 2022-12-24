from typing import Any, List

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from auto_mobile.db import dependencies
from auto_mobile.db.models import Script
from auto_mobile.db.repositoies.script_repo import ScriptRepository
from sqlalchemy.orm import Session

from auto_mobile.web.schema.script_vo import ScriptVO
from loguru import logger
router = APIRouter()


@router.get("/", response_model= List[ScriptVO], status_code=201)
def get_scripts(
    db :Session = Depends(dependencies.get_db_session) ,
    page_size: int = 100,
    page: int = 1
) -> Any:
    """
    Get Scripts
    """
    scriptRepo = ScriptRepository(Script)
    results =  scriptRepo.get_multi(db,page,page_size)
    return results
    


@router.post("/", response_model= ScriptVO, status_code=201)
def create_scripts(
    *,
    db :Session = Depends(dependencies.get_db_session) ,
    scriptVO: ScriptVO
) -> Any:
    """
    Create Scripts
    """
    scriptRepo = ScriptRepository(Script)
    return scriptRepo.create(db = db,obj_in = scriptVO)

@router.put("/", response_model= ScriptVO, status_code=201)
def update_scripts(
    *,
    db :Session = Depends(dependencies.get_db_session) ,
    scriptVO: ScriptVO
) -> Any:
    """
    Create Scripts
    """
    scriptRepo = ScriptRepository(Script)
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
    scriptRepo = ScriptRepository(Script)
    scriptRepo.remove(db = db,id= id)

    return "delete OK"


@router.get("/{id}", response_model= ScriptVO, status_code=201)
def delete_scripts(
    id: int, 
    db :Session = Depends(dependencies.get_db_session) ,  
) -> Any:
    """
    Create Scripts
    """
    scriptRepo = ScriptRepository(Script)
    return scriptRepo.get(db = db,id= id)