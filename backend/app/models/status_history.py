from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    status = Column(String(50), nullable=False)
    changed_at = Column(DateTime, server_default=func.now())

    application = relationship("Application", back_populates="status_history")