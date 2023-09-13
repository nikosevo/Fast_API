from pydantic import BaseModel
from typing import Optional



class ARTICLE(BaseModel):
    title: str
    topic: int
    content: str

class COMMENT(BaseModel):
    username: Optional[str] = None
    content:str