from sqlalchemy.orm import Session
from backend.models.models import Listener
from backend.schemas.user import ListenerCreate
from sqlalchemy import or_

def create_listener(db: Session, listener: ListenerCreate):
    db_listener = Listener(username=listener.username, email=listener.email, password=listener.password)
    db.add(db_listener)
    db.commit()
    db.refresh(db_listener)
    return db_listener

def login_listener(db: Session, email: str, password: str):
    return db.query(Listener).filter(Listener.email == email, Listener.password == password).first()


def follow_playlist(db: Session, listener_id: int, playlist_id: int):
    from backend.models.models import Follow
    follow = Follow(listener_id=listener_id, playlist_id=playlist_id)
    db.add(follow)
    db.commit()
    return follow

def unfollow_playlist(db: Session, listener_id: int, playlist_id: int):
    from backend.models.models import Follow
    follow = db.query(Follow).filter(Follow.listener_id == listener_id, Follow.playlist_id == playlist_id).first()
    if not follow:
        raise ValueError("Follow relationship does not exist")
    db.delete(follow)
    db.commit()
    return {"message": "Unfollowed successfully"}

def user_info_by_email(db: Session, email: str):
    return db.query(Listener).filter(Listener.email == email).first()