from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from backend.models.models import Song, Playback, Playlist, Follow, Listener


def get_most_played_songs(db: Session):
    one_week_ago = datetime.utcnow() - timedelta(days=40)
    return (
        db.query(
            Song.id,
            Song.title,
            Song.artist,
            Song.album,
            Song.duration,
            func.sum(Playback.duration_played).label("total_play_time"),
            Song.url,
            Song.image_url
        )
        .join(Playback, Song.id == Playback.song_id)
        .filter(Playback.played_at >= one_week_ago)
        .group_by(Song.id)
        .order_by(func.sum(Playback.duration_played).desc())
        .limit(10)
        .all()
    )

def get_user_playtime(db: Session):
    return (
        db.query(
            Listener.id.label("listener_id"),
            Listener.username,
            func.sum(Playback.duration_played).label("total_playtime")
        )
        .join(Playback, Listener.id == Playback.listener_id)
        .group_by(Listener.id)
        .order_by(func.sum(Playback.duration_played).desc())
        .all()
    )

def get_top_playlists(db: Session):
    return (
        db.query(
            Playlist.id,
            Playlist.name,
            func.count(Follow.listener_id).label("follower_count"),
            Listener.username.label("created_by")
        )
        .join(Listener, Playlist.listener_id == Listener.id)
        .join(Follow, Playlist.id == Follow.playlist_id)
        .group_by(Playlist.id, Listener.username)
        .order_by(func.count(Follow.listener_id).desc())
        .limit(10)
        .all()
    )

def get_listener_playlist_follows(db: Session, listener_id: int):
    playlists = (
        db.query(
            Playlist.id,
            Playlist.name,
            Listener.username.label("created_by")
        )
        .join(Listener, Playlist.listener_id == Listener.id)
        .filter(Follow.listener_id == listener_id, Follow.playlist_id == Playlist.id)
        .group_by(Playlist.id, Listener.username)
        .all()
    )

    return [
        {
            "id": playlist.id,
            "name": playlist.name,
            "created_by": playlist.created_by,
            "follower_count": db.query(func.count(Follow.listener_id))
            .filter(Follow.playlist_id == playlist.id)
            .scalar()
        }
        for playlist in playlists
    ]
