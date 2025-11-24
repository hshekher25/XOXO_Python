from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.profile import ProfileResponse


class LocationUpdate(BaseModel):
    latitude: float
    longitude: float


class NearbyUserResponse(BaseModel):
    user_id: str
    profile: ProfileResponse
    distance_km: float


class NearbyChatResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


class NearbyChatMessageCreate(BaseModel):
    message: str


class NearbyChatMessageResponse(BaseModel):
    id: str
    chat_id: str
    sender_id: str
    sender_name: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

