from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ListenerCreate(BaseModel):
    username: str
    email: str
    password: str

class ListenerLogin(BaseModel):
    email: str
    password: str

class PlaylistCreate(BaseModel):
    name: str
    listener_id: int

class PlaylistResponse(BaseModel):
    id: int
    name: str
    listener_id: int
    created_at: datetime
    is_user_created: bool
    class Config:
        from_attributes = True

class SongResponse(BaseModel):
    id: int
    title: str
    artist: Optional[str] = None
    album: Optional[str] = None  # This is the key line
    duration: int
    url: Optional[str] = None
    image_url: Optional[str] = None
    class Config:
        orm_mode = True


class PlaybackCreate(BaseModel):
    listener_id: int
    song_id: int
    duration_played: int