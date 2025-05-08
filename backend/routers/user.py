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
