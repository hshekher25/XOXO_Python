from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.swipe import Match
from app.models.chat import ChatMessage
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse

router = APIRouter()


@router.post("/{match_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    match_id: str,
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify match exists and user is part of it
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    
    if match.user1_id != current_user.id and match.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not part of this match",
        )
    
    chat_message = ChatMessage(
        match_id=match_id,
        sender_id=current_user.id,
        message=message_data.message,
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message


@router.get("/{match_id}/messages", response_model=List[ChatMessageResponse])
async def get_messages(
    match_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify match exists and user is part of it
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    
    if match.user1_id != current_user.id and match.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not part of this match",
        )
    
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.match_id == match_id)
        .order_by(ChatMessage.created_at)
        .all()
    )
    return messages

