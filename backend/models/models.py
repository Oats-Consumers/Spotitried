from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Listener(Base):
    __tablename__ = "listener"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    playlists = relationship("Playlist", back_populates="listener")
    playbacks = relationship("Playback", back_populates="listener")
    follows = relationship("Follow", back_populates="listener")


class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    is_user_created = Column(Boolean, default=True)
    listener_id = Column(Integer, ForeignKey("listener.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    listener = relationship("Listener", back_populates="playlists")
    songs = relationship("PlaylistSong", back_populates="playlist")
    followers = relationship("Follow", back_populates="playlist")


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    artist = Column(String(100))
    album = Column(String(100))
    duration = Column(Integer, nullable=False)
    url = Column(String, unique=True, nullable=False)
    image_url = Column(String)

    playbacks = relationship("Playback", back_populates="song")
    playlists = relationship("PlaylistSong", back_populates="song")


class Playback(Base):
    __tablename__ = "playback"

    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, ForeignKey("listener.id"))
    song_id = Column(Integer, ForeignKey("song.id"))
    played_at = Column(DateTime, default=datetime.utcnow)
    duration_played = Column(Integer, nullable=False)

    listener = relationship("Listener", back_populates="playbacks")
    song = relationship("Song", back_populates="playbacks")


class PlaylistSong(Base):
    __tablename__ = "playlistsong"

    playlist_id = Column(Integer, ForeignKey("playlist.id"), primary_key=True)
    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    added_at = Column(DateTime, default=datetime.utcnow)

    playlist = relationship("Playlist", back_populates="songs")
    song = relationship("Song", back_populates="playlists")


class Follow(Base):
    __tablename__ = "follow"

    listener_id = Column(Integer, ForeignKey("listener.id"), primary_key=True)
    playlist_id = Column(Integer, ForeignKey("playlist.id"), primary_key=True)
    followed_at = Column(DateTime, default=datetime.utcnow)

    listener = relationship("Listener", back_populates="follows")
    playlist = relationship("Playlist", back_populates="followers")
