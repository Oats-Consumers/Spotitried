from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import PlaylistCreate, PlaylistResponse, PlaybackCreate, SongResponse, ListenerCreate, ListenerLogin
from backend.crud import user

router = APIRouter()

@router.post("/playlist", response_model=PlaylistResponse)
def create_playlist(playlist: PlaylistCreate, db: Session = Depends(get_db)):
    return user.create_playlist(db, playlist)

@router.delete("/playlist/{playlist_id}")
def delete_playlist(playlist_id: int, db: Session = Depends(get_db)):
    result = user.delete_playlist(db, playlist_id)
    if not result:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return {"message": "Playlist deleted successfully"}

@router.get("/playlist/{playlist_id}/songs", response_model=list[SongResponse])
def get_songs_in_playlist(playlist_id: int, db: Session = Depends(get_db)):
    return user.get_songs_in_playlist(db, playlist_id)

@router.post("/playback")
def create_playback(playback: PlaybackCreate, db: Session = Depends(get_db)):
    return user.create_playback(db, playback.listener_id, playback.song_id, playback.duration_played)

@router.get("/search", response_model=list[SongResponse])
def search_songs(query: str, db: Session = Depends(get_db)):
    return user.search_songs_by_name(db, query)

@router.post("/register")
def register_listener(listener_data: ListenerCreate, db: Session = Depends(get_db)):
    return user.create_listener(db, listener_data)

@router.post("/login")
def login_listener(credentials: ListenerLogin, db: Session = Depends(get_db)):
    db_listener = user.login_listener(db, credentials.email, credentials.password)
    if not db_listener:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "listener_id": db_listener.id}
