from sqlalchemy.orm import Session
from backend.models.models import Song, Playback
from datetime import datetime

def create_playback(db: Session, listener_id: int, song_id: int, duration_played: int):
    playback = Playback(
        listener_id=listener_id,
        song_id=song_id,
        duration_played=duration_played,
        played_at=datetime.utcnow()
    )
    db.add(playback)
    db.commit()
    db.refresh(playback)
    return playback

def search_songs_by_name(db: Session, query: str):
    return db.query(Song).filter(Song.title.ilike(f"%{query}%")).all()