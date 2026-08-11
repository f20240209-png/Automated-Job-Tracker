from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationResponse)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    new_app = Application(**payload.model_dump())
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app


@router.get("/", response_model=list[ApplicationResponse])
def list_applications(db: Session = Depends(get_db)):
    return db.scalars(select(Application)).all()


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    app_obj = db.get(Application, application_id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj