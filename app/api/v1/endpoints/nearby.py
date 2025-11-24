from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.redis_client import redis_client
from app.models.user import User
from app.models.profile import Profile
from app.models.nearby_chat import NearbyChat, NearbyChatMessage
from app.schemas.nearby import (
    LocationUpdate,
    NearbyUserResponse,
    NearbyChatResponse,
    NearbyChatMessageCreate,
    NearbyChatMessageResponse,
)
from app.services.location_service import LocationService

router = APIRouter()


@router.post("/location")
async def update_location(
    location: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Update profile location
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    
    profile.latitude = location.latitude
    profile.longitude = location.longitude
    db.commit()
    
    # Update Redis for presence
    redis_key = f"user:location:{current_user.id}"
    redis_client.setex(
        redis_key,
        3600,  # 1 hour TTL
        f"{location.latitude},{location.longitude}",
    )
    
    return {"message": "Location updated"}


@router.get("/users", response_model=List[NearbyUserResponse])
async def get_nearby_users(
    radius_km: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get current user's profile
    my_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not my_profile or not my_profile.latitude or not my_profile.longitude:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please update your location first",
        )
    
    location_service = LocationService()
    nearby_users = location_service.find_nearby_users(
        db,
        my_profile.latitude,
        my_profile.longitude,
        radius_km,
        exclude_user_id=current_user.id,
    )
    
    return nearby_users


@router.get("/chat", response_model=NearbyChatResponse)
async def get_or_create_nearby_chat(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check for existing active nearby chat
    active_chat = (
        db.query(NearbyChat)
        .filter(NearbyChat.expires_at > datetime.utcnow())
        .order_by(NearbyChat.created_at.desc())
        .first()
    )
    
    if active_chat:
        return active_chat
    
    # Create new nearby chat (expires in 24 hours)
    new_chat = NearbyChat(
        name=f"Nearby Chat - {datetime.utcnow().strftime('%Y-%m-%d')}",
        expires_at=datetime.utcnow() + timedelta(hours=24),
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


@router.post("/chat/{chat_id}/messages", response_model=NearbyChatMessageResponse)
async def send_nearby_chat_message(
    chat_id: str,
    message_data: NearbyChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify chat exists and is active
    chat = db.query(NearbyChat).filter(NearbyChat.id == chat_id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    if chat.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat has expired",
        )
    
    # Get sender name
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    sender_name = profile.name if profile else current_user.email
    
    chat_message = NearbyChatMessage(
        chat_id=chat_id,
        sender_id=current_user.id,
        sender_name=sender_name,
        message=message_data.message,
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message


@router.get("/chat/{chat_id}/messages", response_model=List[NearbyChatMessageResponse])
async def get_nearby_chat_messages(
    chat_id: str,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    chat = db.query(NearbyChat).filter(NearbyChat.id == chat_id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    messages = (
        db.query(NearbyChatMessage)
        .filter(NearbyChatMessage.chat_id == chat_id)
        .order_by(NearbyChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(messages))

