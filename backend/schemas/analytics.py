from pydantic import BaseModel
from typing import Optional

class SongStat(BaseModel):
    id: int
    title: str
    artist: Optional[str] = None
    album: Optional[str] = None
    duration: int
    total_play_time: float
    class Config:
        from_attributes = True


class UserPlaytime(BaseModel):
    listener_id: int
    username: str
    total_playtime: float

    class Config:
        from_attributes = True

class PlaylistStat(BaseModel):
    id: int
    name: str
    created_by: str
    follower_count: int
    class Config:
        from_attributes = True
