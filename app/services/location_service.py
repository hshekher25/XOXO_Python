from sqlalchemy.orm import Session
from geopy.distance import geodesic
from typing import List
from app.models.profile import Profile
from app.schemas.nearby import NearbyUserResponse
from app.schemas.profile import ProfileResponse


class LocationService:
    def find_nearby_users(
        self,
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: int,
        exclude_user_id: str,
    ) -> List[NearbyUserResponse]:
        # Get all active profiles with location
        profiles = (
            db.query(Profile)
            .filter(
                Profile.user_id != exclude_user_id,
                Profile.is_active == True,
                Profile.latitude.isnot(None),
                Profile.longitude.isnot(None),
            )
            .all()
        )
        
        nearby_users = []
        user_location = (latitude, longitude)
        
        for profile in profiles:
            profile_location = (profile.latitude, profile.longitude)
            distance = geodesic(user_location, profile_location).kilometers
            
            if distance <= radius_km:
                nearby_users.append(
                    NearbyUserResponse(
                        user_id=str(profile.user_id),
                        profile=ProfileResponse.from_orm(profile),
                        distance_km=round(distance, 2),
                    )
                )
        
        # Sort by distance
        nearby_users.sort(key=lambda x: x.distance_km)
        return nearby_users

