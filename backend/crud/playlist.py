from sqlalchemy.orm import Session
from backend.models.models import Song, Playlist, Listener, PlaylistSong, Follow
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

def get_playlist_by_id(db: Session, playlist_id: int):
    playlist = db.query(
        Playlist.id,
        Playlist.name,
        Playlist.is_user_created,
        Playlist.listener_id,
        Playlist.created_at
    ).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise ValueError("Playlist not found")
    return playlist

def followers_of_playlist(db: Session, playlist_id: int, listener_id: int):
    follower_count = db.query(func.count(Follow.listener_id)).filter(Follow.playlist_id == playlist_id).scalar()
    created_by = db.query(Listener.username).filter(Listener.id == listener_id).scalar()
    print(f"first Follower count: {follower_count}, Created by: {created_by}")
    return follower_count, created_by

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

def get_playlist_by_name(db: Session, pattern: str):
    wildcard_pattern = f"%{pattern}%"
    return db.query(Playlist).filter(Playlist.name.ilike(wildcard_pattern)).all()

def add_song_to_playlist(db: Session, playlist_id: int, song_id: int):
    link = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
    db.add(link)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Song already exists in playlist")
    return link

def remove_song_from_playlist(db: Session, playlist_id: int, song_id: int):
    link = db.query(PlaylistSong).filter_by(playlist_id=playlist_id, song_id=song_id).first()
    if not link:
        raise ValueError("Song not found in playlist")
    db.delete(link)
    db.commit()
    return True