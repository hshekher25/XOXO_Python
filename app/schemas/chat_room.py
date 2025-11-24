from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRoomCreate(BaseModel):
    name: str
    topic: Optional[str] = None
    description: Optional[str] = None


class ChatRoomResponse(BaseModel):
    id: str
    name: str
    topic: Optional[str]
    description: Optional[str]
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRoomMessageCreate(BaseModel):
    message: str


class ChatRoomMessageResponse(BaseModel):
    id: str
    room_id: str
    sender_id: str
    sender_name: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

