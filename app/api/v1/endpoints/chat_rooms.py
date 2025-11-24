from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.profile import Profile
from app.models.chat_room import ChatRoom, ChatRoomMessage
from app.schemas.chat_room import (
    ChatRoomCreate,
    ChatRoomResponse,
    ChatRoomMessageCreate,
    ChatRoomMessageResponse,
)

router = APIRouter()


@router.post("", response_model=ChatRoomResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_room(
    room_data: ChatRoomCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if room name already exists
    existing_room = db.query(ChatRoom).filter(ChatRoom.name == room_data.name).first()
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat room name already exists",
        )
    
    room = ChatRoom(
        name=room_data.name,
        topic=room_data.topic,
        description=room_data.description,
        created_by=current_user.id,
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.get("", response_model=List[ChatRoomResponse])
async def list_chat_rooms(db: Session = Depends(get_db)):
    rooms = db.query(ChatRoom).all()
    return rooms


@router.get("/{room_id}", response_model=ChatRoomResponse)
async def get_chat_room(room_id: str, db: Session = Depends(get_db)):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found",
        )
    return room


@router.post("/{room_id}/messages", response_model=ChatRoomMessageResponse)
async def send_room_message(
    room_id: str,
    message_data: ChatRoomMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify room exists
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found",
        )
    
    # Get sender name from profile
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    sender_name = profile.name if profile else current_user.email
    
    room_message = ChatRoomMessage(
        room_id=room_id,
        sender_id=current_user.id,
        sender_name=sender_name,
        message=message_data.message,
    )
    db.add(room_message)
    db.commit()
    db.refresh(room_message)
    return room_message


@router.get("/{room_id}/messages", response_model=List[ChatRoomMessageResponse])
async def get_room_messages(
    room_id: str,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found",
        )
    
    messages = (
        db.query(ChatRoomMessage)
        .filter(ChatRoomMessage.room_id == room_id)
        .order_by(ChatRoomMessage.created_at.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(messages))

