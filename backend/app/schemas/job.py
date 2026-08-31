from pydantic import BaseModel
from typing import Optional


class JobCreate(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    link: Optional[str] = None
    salary: Optional[str] = None
    job_type: Optional[str] = None



class JobResponse(BaseModel):
    id: int
    company: str
    role: str
    location: Optional[str] = None
    link: Optional[str] = None
    ai_score: Optional[int] = None

    class Config:
        from_attributes = True        