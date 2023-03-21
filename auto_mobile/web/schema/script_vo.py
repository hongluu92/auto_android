from typing import Optional
from pydantic import BaseModel
from typing import Any, List

class ScriptVO(BaseModel):
    __tablename__ = "scripts"

    id: int = None
    name: str = ""
    game: Optional[str] = None
    loop: int = 0
    loop_delay: int = 1000
    class Config:
        orm_mode = True

class ScriptRefVO :
    child_id: int 
    parrent: int = None
    loop: int = 1
    loop_delay = 1000