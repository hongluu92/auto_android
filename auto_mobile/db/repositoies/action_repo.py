from typing import List
from .base_repo import BaseRepository
from ..models.action import Action
from auto_mobile.web.schema.action import ActionVO, ActionVOCreated
from sqlalchemy.orm import Session

class ActionRepository(BaseRepository[Action, ActionVOCreated, ActionVOCreated]):
    def __init__(self ):
        super().__init__(Action)
        
    def get_multi_by_script_id(self, db: Session,script_id, offset: int = 0, limit: int = 100) -> List[Action]:
        return db.query(self.model).filter(self.model.script_id == script_id).offset(offset).limit(limit).all()
