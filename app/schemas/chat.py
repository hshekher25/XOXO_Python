from pydantic import BaseModel
from datetime import datetime


class ChatMessageCreate(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    id: str
    match_id: str
    sender_id: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

