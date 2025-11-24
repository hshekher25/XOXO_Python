from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.profile import ProfileResponse


class SwipeCreate(BaseModel):
    swiped_id: str
    is_like: bool


class SwipeResponse(BaseModel):
    swipe: dict
    is_match: bool
    match_id: Optional[str] = None


class MatchResponse(BaseModel):
    match_id: str
    user_id: str
    profile: ProfileResponse
    created_at: datetime

