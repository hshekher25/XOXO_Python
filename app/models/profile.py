from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    bio = Column(Text, nullable=True)
    gender = Column(String(50), nullable=False)  # 'male', 'female', 'non-binary', etc.
    gender_preference = Column(String(50), nullable=False)  # 'male', 'female', 'all'
    photos = Column(JSON, default=list)  # Array of S3 URLs (stored as JSON text in MariaDB)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    max_distance_km = Column(Integer, default=50)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", backref="profile")

