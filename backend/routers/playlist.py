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


@router.get("/get_by_name/{name}", response_model=list[PlaylistResponse])
def get_playlist_by_name(name: str, db: Session = Depends(get_db)):
    playlist = func_playlist.get_playlist_by_name(db, name)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist

@router.post("/{playlist_id}/songs/{song_id}")
def add_song(playlist_id: int, song_id: int, db: Session = Depends(get_db)):
    try:
        return func_playlist.add_song_to_playlist(db, playlist_id, song_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{playlist_id}/songs/{song_id}")
def delete_song(playlist_id: int, song_id: int, db: Session = Depends(get_db)):
    try:
        func_playlist.remove_song_from_playlist(db, playlist_id, song_id)
        return {"detail": "Song removed"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))