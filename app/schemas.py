# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class UserQuery(BaseModel):
    text: str

class Recommendation(BaseModel):
    item_id: int
    title: str
    score: float
    domain: str

class Feedback(BaseModel):
    item_id: int
    domain: str
    liked: bool
