from .base_repo import BaseRepository
from ..models.script import Script
from sqlalchemy.orm import Session
from ...web.schema.script_vo import ScriptVO

class ScriptRepository(BaseRepository[Script, ScriptVO, ScriptVO]):
   pass
