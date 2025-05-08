from sqlalchemy.orm import Session
from backend.models.models import Playlist, Song, PlaylistSong, Playback, Listener
from backend.schemas.user import PlaylistCreate, ListenerCreate
from datetime import datetime
from sqlalchemy import or_

def create_playlist(db: Session, playlist_data: PlaylistCreate):
    listener = db.query(Listener).filter(Listener.id == playlist_data.listener_id).first()
    if not listener:
        raise ValueError(f"Listener with ID {playlist_data.listener_id} does not exist")

    playlist = Playlist(
        name=playlist_data.name,
        listener_id=playlist_data.listener_id,
        created_at=datetime.utcnow()
    )
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist

def delete_playlist(db: Session, playlist_id: int):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if playlist:
        db.delete(playlist)
        db.commit()
    return playlist

def get_songs_in_playlist(db: Session, playlist_id: int):
    return (
        db.query(Song)
        .join(PlaylistSong, Song.id == PlaylistSong.song_id)
        .filter(PlaylistSong.playlist_id == playlist_id)
        .order_by(PlaylistSong.added_at)
        .all()
    )

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

def create_listener(db: Session, listener: ListenerCreate):
    db_listener = Listener(username=listener.username, email=listener.email, password=listener.password)
    db.add(db_listener)
    db.commit()
    db.refresh(db_listener)
    return db_listener

def login_listener(db: Session, email: str, password: str):
    return db.query(Listener).filter(Listener.email == email, Listener.password == password).first()
