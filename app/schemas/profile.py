from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime


class ProfileCreate(BaseModel):
    name: str
    age: int
    bio: Optional[str] = None
    gender: str
    gender_preference: str
    max_distance_km: int = 50


class ProfileImageUpdate(BaseModel):
    url: str
    isMain: Optional[bool] = Field(default=False, alias="isMain")
    order: Optional[int] = Field(default=0, alias="order")
    caption: Optional[str] = None

    class Config:
        populate_by_name = True  # Allow both snake_case and camelCase


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    bio: Optional[str] = None
    gender: Optional[str] = None
    gender_preference: Optional[str] = Field(None, alias="genderPreference")
    max_distance_km: Optional[int] = Field(None, alias="maxDistanceKm")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    images: Optional[List[ProfileImageUpdate]] = None

    class Config:
        populate_by_name = True  # Allow both snake_case and camelCase


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    name: str
    age: int
    bio: Optional[str]
    gender: str
    gender_preference: str
    photos: List[str]
    latitude: Optional[float]
    longitude: Optional[float]
    max_distance_km: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

