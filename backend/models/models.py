from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class Playback(Base):
    __tablename__ = "playback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    song_id = Column(Integer, ForeignKey("song.id"))
    played_at = Column(DateTime)
    duration_played = Column(Integer)

class Follow(Base):
    __tablename__ = "follow"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    playlist_id = Column(Integer, ForeignKey("playlist.id"), primary_key=True)
    followed_at = Column(DateTime)

class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    duration = Column(Integer)
    
class Playlist(Base):
    __tablename__ = "playlist"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_by_user_id = Column(Integer, ForeignKey("user.id"))

