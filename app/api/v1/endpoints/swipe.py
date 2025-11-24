from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.profile import Profile
from app.models.swipe import Swipe, Match
from app.schemas.swipe import SwipeCreate, SwipeResponse, MatchResponse

router = APIRouter()


@router.post("", response_model=SwipeResponse)
async def create_swipe(
    swipe_data: SwipeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if already swiped
    existing_swipe = (
        db.query(Swipe)
        .filter(
            Swipe.swiper_id == current_user.id,
            Swipe.swiped_id == swipe_data.swiped_id,
        )
        .first()
    )
    if existing_swipe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already swiped on this user",
        )
    
    # Create swipe
    swipe = Swipe(
        swiper_id=current_user.id,
        swiped_id=swipe_data.swiped_id,
        is_like=swipe_data.is_like,
    )
    db.add(swipe)
    
    # Check for match (if like and other user also liked)
    if swipe_data.is_like:
        mutual_swipe = (
            db.query(Swipe)
            .filter(
                Swipe.swiper_id == swipe_data.swiped_id,
                Swipe.swiped_id == current_user.id,
                Swipe.is_like == True,
            )
            .first()
        )
        if mutual_swipe:
            # Create match
            match = Match(user1_id=current_user.id, user2_id=swipe_data.swiped_id)
            db.add(match)
            db.commit()
            return {"swipe": swipe, "is_match": True, "match_id": str(match.id)}
    
    db.commit()
    return {"swipe": swipe, "is_match": False, "match_id": None}


@router.get("/matches", response_model=List[MatchResponse])
async def get_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    matches = (
        db.query(Match)
        .filter(
            (Match.user1_id == current_user.id) | (Match.user2_id == current_user.id)
        )
        .all()
    )
    
    result = []
    for match in matches:
        other_user_id = (
            match.user2_id if match.user1_id == current_user.id else match.user1_id
        )
        other_profile = db.query(Profile).filter(Profile.user_id == other_user_id).first()
        result.append(
            {
                "match_id": str(match.id),
                "user_id": str(other_user_id),
                "profile": other_profile,
                "created_at": match.created_at,
            }
        )
    
    return result

