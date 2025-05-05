from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from backend.models.models import Song, Playback, Playlist, Follow


def get_most_played_songs(db: Session):
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    return (
        db.query(Song.id, Song.title, func.count(Playback.id).label("play_count"))
        .join(Playback, Song.id == Playback.song_id)
        .filter(Playback.played_at >= one_week_ago)
        .group_by(Song.id)
        .order_by(func.count(Playback.id).desc())
        .limit(10)
        .all()
    )

def get_user_playtime(db: Session):
    first_day_last_month = (datetime.utcnow().replace(day=1) - timedelta(days=1)).replace(day=1)
    first_day_this_month = datetime.utcnow().replace(day=1)

    return (
        db.query(Playback.user_id, func.sum(Playback.duration_played).label("total_playtime"))
        .filter(Playback.played_at >= first_day_last_month)
        .filter(Playback.played_at < first_day_this_month)
        .group_by(Playback.user_id)
        .all()
    )

def get_top_playlists(db: Session):
    return (
        db.query(Playlist.id, Playlist.name, func.count(Follow.user_id).label("follower_count"))
        .join(Follow, Playlist.id == Follow.playlist_id)
        .group_by(Playlist.id)
        .order_by(func.count(Follow.user_id).desc())
        .limit(10)
        .all()
    )
