from pydantic import BaseModel
from typing import List, Optional

class ClassOut(BaseModel):
    id: int
    name: str

class UserBrief(BaseModel):
    id: int
    full_name: str
    rank: int
    avg_speed: float
    correct_answers: int

class UserDetail(BaseModel):
    id: int
    tg_username: Optional[str]
    full_name: str
    correct_answers: int
    total_time_seconds: float
    answers: List[dict]
