from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.scoring import score_job

from app.database import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse
from app.auth import get_current_user, verify_api_key

router = APIRouter(prefix="/jobs", tags=["jobs"])


NEARBY_SUBURBS = [
    "melbourne", "southbank", "docklands", "south wharf", "west melbourne",
    "north melbourne", "kensington", "flemington", "parkville", "carlton",
    "fitzroy", "collingwood", "abbotsford", "richmond", "cremorne",
    "south yarra", "toorak", "prahran", "windsor", "st kilda", "balaclava",
    "elwood", "albert park", "middle park", "port melbourne", "south melbourne",
    "east melbourne", "brunswick", "northcote", "coburg", "kew", "hawthorn",
    "malvern", "armadale", "caulfield", "elsternwick", "moonee ponds",
    "ascot vale", "yarraville", "footscray", "seddon", "kingsville",
    "spotswood", "carlton north", "fitzroy north",
]


def is_relevant(location: str | None) -> bool:
    if not location:
        return False
    location_lower = location.lower()
    return any(suburb in location_lower for suburb in NEARBY_SUBURBS)


@router.post("/new", dependencies=[Depends(verify_api_key)])
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    if not is_relevant(payload.location):
        return {"status": "skipped", "reason": "outside ~10km of 3006"}

    score, reason = score_job(payload.role, payload.company, payload.location or "")

    extra_notes = [reason]
    if payload.salary:
        extra_notes.append(f"Salary: {payload.salary}")
    if payload.job_type:
        extra_notes.append(f"Job type: {payload.job_type}")

    new_job = Job(
        company=payload.company,
        role=payload.role,
        location=payload.location,
        link=payload.link,
        ai_score=score,
        ai_reason=" | ".join(extra_notes),
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"status": "saved", "job": JobResponse.model_validate(new_job)}


@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.scalars(select(Job)).all()