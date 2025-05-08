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
