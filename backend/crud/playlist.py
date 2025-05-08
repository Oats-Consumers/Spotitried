from sqlalchemy.orm import Session
from backend.models.models import Song, Playlist, Listener, PlaylistSong
from datetime import datetime
from sqlalchemy.exc import IntegrityError

def add_song_to_playlist(db: Session, playlist_id: int, song_id: int):
    playlist_song = PlaylistSong(
        playlist_id=playlist_id,
        song_id=song_id,
        added_at=datetime.utcnow()
    )
    db.add(playlist_song)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Song is already in the playlist")
    return playlist_song

def remove_song_from_playlist(db: Session, playlist_id: int, song_id: int):
    entry = db.query(PlaylistSong).filter_by(
        playlist_id=playlist_id,
        song_id=song_id
    ).first()
    if entry:
        db.delete(entry)
        db.commit()
        return {"message": "Song removed"}
    else:
        raise ValueError("Song not found in playlist")


def create_playlist(db: Session, playlist_data: Playlist):
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