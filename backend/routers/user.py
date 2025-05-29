from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import ListenerCreate, ListenerLogin
from backend.crud import user

router = APIRouter()

@router.post("/register")
def register_listener(listener_data: ListenerCreate, db: Session = Depends(get_db)):
    return user.create_listener(db, listener_data)

@router.post("/login")
def login_listener(credentials: ListenerLogin, db: Session = Depends(get_db)):
    db_listener = user.login_listener(db, credentials.email, credentials.password)
    if not db_listener:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "listener_id": db_listener.id}

@router.get("/follow/{listener_id}/{playlist_id}")
def follow_playlist(listener_id: int, playlist_id: int, db: Session = Depends(get_db)):
    return user.follow_playlist(db, listener_id, playlist_id)

@router.get("/unfollow/{listener_id}/{playlist_id}")
def unfollow_playlist(listener_id: int, playlist_id: int, db: Session = Depends(get_db)):
    return user.unfollow_playlist(db, listener_id, playlist_id)

@router.get("/user-info-by-mail/{mail}")
def user_info_by_mail(mail: str, db: Session = Depends(get_db)):
    db_listener = user.user_info_by_mail(db, mail)
    if not db_listener:
        raise HTTPException(status_code=404, detail="User not found")
    return db_listener