from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.analytics import SongStat, UserPlaytime, PlaylistStat
from backend.crud import analytics

router = APIRouter()

@router.get("/most-played-songs", response_model=list[SongStat])
def get_most_played_songs(db: Session = Depends(get_db)):
    return analytics.get_most_played_songs(db)

@router.get("/user-playtime", response_model=list[UserPlaytime])
def get_user_playtime(db: Session = Depends(get_db)):
    return analytics.get_user_playtime(db)

@router.get("/top-playlists", response_model=list[PlaylistStat])
def get_top_playlists(db: Session = Depends(get_db)):
    return analytics.get_top_playlists(db)
