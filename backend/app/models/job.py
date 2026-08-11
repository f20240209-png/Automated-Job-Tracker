
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    location = Column(String(255))
    link = Column(String(500))
    posted_date = Column(Date)
    ai_score = Column(Integer)
    ai_reason = Column(Text)

    applications = relationship("Application", back_populates="job")