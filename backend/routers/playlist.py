from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import PlaylistCreate, PlaylistResponse, SongResponse
from backend.crud import playlist as func_playlist

router = APIRouter()

@router.post("/create", response_model=PlaylistResponse)
def create_playlist(playlist: PlaylistCreate, db: Session = Depends(get_db)):
    return func_playlist.create_playlist(db, playlist)

@router.delete("/delete/{playlist_id}")
def delete_playlist(playlist_id: int, db: Session = Depends(get_db)):
    result = func_playlist.delete_playlist(db, playlist_id)
    if not result:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return {"message": "Playlist deleted successfully"}

@router.get("/get/{playlist_id}/songs", response_model=list[SongResponse])
def get_songs_in_playlist(playlist_id: int, db: Session = Depends(get_db)):
    return func_playlist.get_songs_in_playlist(db, playlist_id)

