from pydantic import BaseModel

class SongStat(BaseModel):
    id: int
    title: str
    play_count: int

    class Config:
        from_attributes = True

class UserPlaytime(BaseModel):
    user_id: int
    total_playtime: float

    class Config:
        from_attributes = True

class PlaylistStat(BaseModel):
    id: int
    name: str
    follower_count: int

    class Config:
        from_attributes = True

