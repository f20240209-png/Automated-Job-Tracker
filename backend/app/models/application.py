from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    status = Column(String(50), default="New", nullable=False)
    applied_date = Column(Date)
    deadline = Column(Date)
    last_follow_up = Column(DateTime)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    status_history = relationship("StatusHistory", back_populates="application")