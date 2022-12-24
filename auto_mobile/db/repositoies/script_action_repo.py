from typing import List
from .base_repo import BaseRepository
from ..models.script_action import ScriptAction
from auto_mobile.web.schema.script_action import ScriptActionVO
from sqlalchemy.orm import Session

class ScriptActionRepository(BaseRepository[ScriptAction, ScriptActionVO, ScriptActionVO]):
    def __init__(self ):
        super().__init__(ScriptAction)
        
    def get_multi_by_script_id(self, db: Session,script_id, offset: int = 0, limit: int = 100) -> List[ScriptAction]:
        return db.query(self.model).filter(self.model.script_id == script_id).offset(offset).limit(limit).all()
