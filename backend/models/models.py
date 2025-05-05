from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'User'  # <- DO NOT manually add quotes
    __table_args__ = {'quote': True}  # <- Let SQLAlchemy quote it automatically
    id = Column(Integer, primary_key=True)
    username = Column(String)

class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    duration = Column(Integer)

class Playback(Base):
    __tablename__ = "playback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('"User".id'))
    song_id = Column(Integer, ForeignKey("song.id"))
    played_at = Column(DateTime, default=datetime.utcnow)
    duration_played = Column(Integer)

class Playlist(Base):
    __tablename__ = "playlist"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_user_created = Column(Boolean)
    user_id = Column(Integer, ForeignKey('"User".id'))
    created_at = Column(DateTime)

class Follow(Base):
    __tablename__ = "follow"
    user_id = Column(Integer, ForeignKey('"User".id'), primary_key=True)
    playlist_id = Column(Integer, ForeignKey("playlist.id"), primary_key=True)
    followed_at = Column(DateTime)