from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from typing import Optional as TypingOptional
from app.services.s3_service import S3Service

router = APIRouter()


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if profile already exists
    existing_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists",
        )
    
    profile = Profile(user_id=current_user.id, **profile_data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Use PUT /profiles/me to create your profile.",
        )
    return profile


@router.put("/me", response_model=ProfileResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Upsert: Get existing profile or create new one
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    
    # Handle images separately if provided (before converting to dict)
    images_data = profile_data.images
    
    # Get update data excluding images
    update_data = profile_data.dict(exclude_unset=True, exclude={"images"})
    
    if not profile:
        # Create new profile - require essential fields
        if not all([update_data.get("name"), update_data.get("age"), 
                   update_data.get("gender"), update_data.get("gender_preference")]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: name, age, gender, gender_preference",
            )
        
        profile = Profile(
            user_id=current_user.id,
            name=update_data.get("name"),
            age=update_data.get("age"),
            bio=update_data.get("bio"),
            gender=update_data.get("gender"),
            gender_preference=update_data.get("gender_preference"),
            max_distance_km=update_data.get("max_distance_km", 50),
            latitude=update_data.get("latitude"),
            longitude=update_data.get("longitude"),
            photos=[]  # Initialize empty photos list
        )
        db.add(profile)
    else:
        # Update existing profile
        for field, value in update_data.items():
            if hasattr(profile, field) and value is not None:
                setattr(profile, field, value)
    
    # Handle images if provided
    if images_data is not None and len(images_data) > 0:
        # Convert ProfileImageUpdate to list of URLs (sorted by order, main image first)
        photo_list = []
        for img in images_data:
            if img.url:
                photo_list.append({
                    "url": img.url,
                    "isMain": img.isMain or False,
                    "order": img.order or 0
                })
        
        # Sort by isMain (main first) then by order
        photo_list.sort(key=lambda x: (not x.get("isMain", False), x.get("order", 0)))
        # Extract just URLs for storage (Profile.photos is JSON array of strings)
        profile.photos = [img["url"] for img in photo_list]
    
    db.commit()
    db.refresh(profile)
    return profile


@router.post("/me/photos", response_model=ProfileResponse)
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    
    s3_service = S3Service()
    photo_url = await s3_service.upload_file(file, f"profiles/{current_user.id}/")
    
    if not profile.photos:
        profile.photos = []
    profile.photos.append(photo_url)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/discover", response_model=List[ProfileResponse])
async def discover_profiles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get current user's profile
    my_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not my_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create your profile first.",
        )
    
    # Query profiles based on preferences
    query = db.query(Profile).filter(
        Profile.user_id != current_user.id,
        Profile.is_active == True,
    )
    
    # Filter by gender preference
    if my_profile.gender_preference != "all":
        query = query.filter(Profile.gender == my_profile.gender_preference)
    
    # TODO: Add distance filtering using Haversine formula
    # TODO: Exclude already swiped profiles
    
    profiles = query.limit(50).all()
    return profiles

