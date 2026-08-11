from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int
    status: str = "New"
    applied_date: Optional[date] = None
    deadline: Optional[date] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    applied_date: Optional[date] = None
    deadline: Optional[date] = None
    last_follow_up: Optional[datetime] = None

    class Config:
        from_attributes = True  # lets Pydantic read directly from SQLAlchemy objects