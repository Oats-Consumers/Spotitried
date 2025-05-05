from pydantic import BaseModel

class SongStat(BaseModel):
    id: int
    title: str
    artist: str
    album: str
    duration: int
    play_count: int

    class Config:
        from_attributes = True

class UserPlaytime(BaseModel):
    user_id: int
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
