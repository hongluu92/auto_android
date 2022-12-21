from base_repo import BaseRepository
from ..models.script_action import ScriptAction
from sqlalchemy.orm import Session

class ScriptActionRepository(BaseRepository):
    def __init__(self, entity:ScriptAction ):
        self.entity = entity

scripActionRepo = ScriptActionRepository(ScriptAction)