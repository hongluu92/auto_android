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
) -> Any:
    """
    Get Scripts
    """
    scriptRepo = ScriptRepository(Script)
    results =  scriptRepo.get_multi(db)
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