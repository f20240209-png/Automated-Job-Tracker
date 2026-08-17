from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=token)