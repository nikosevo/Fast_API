from pydantic import BaseModel
from typing import Optional



class ARTICLE(BaseModel):
    title: str
    topic: int
    content: str

class COMMENT(BaseModel):
    username: Optional[str] = None
    content:str

class TOPIC(BaseModel):
    parentTopic: Optional[int] = None
    topic_name: str

class USER(BaseModel):
    username: str
    password: str


class DENIED(BaseModel):
    reason: str