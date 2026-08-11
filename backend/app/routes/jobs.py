from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/new", response_model=JobResponse)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    extra_notes = []
    if payload.salary:
        extra_notes.append(f"Salary: {payload.salary}")
    if payload.job_type:
        extra_notes.append(f"Job type: {payload.job_type}")

    new_job = Job(
        company=payload.company,
        role=payload.role,
        location=payload.location,
        link=payload.link,
        ai_reason=" | ".join(extra_notes) if extra_notes else None,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    return db.scalars(select(Job)).all()