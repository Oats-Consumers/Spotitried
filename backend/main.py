from fastapi import FastAPI
from backend.routers import analytics
from backend.routers import user
from backend.routers import playlist
from backend.routers import basic
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Music Streaming Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(playlist.router, prefix="/playlist", tags=["Playlist"])
app.include_router(basic.router, prefix="/basic", tags=["Basic"])

@app.get("/")
def root():
    return {"message": "Welcome to the Music Streaming Analytics API"}
