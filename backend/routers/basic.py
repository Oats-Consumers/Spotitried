from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import PlaybackCreate, SongResponse
from backend.crud import basic

router = APIRouter()

@router.post("/playback")
def create_playback(playback: PlaybackCreate, db: Session = Depends(get_db)):
    return basic.create_playback(db, playback.listener_id, playback.song_id, playback.duration_played)

@router.get("/search", response_model=list[SongResponse])
def search_songs(query: str, db: Session = Depends(get_db)):
    return basic.search_songs_by_name(db, query)