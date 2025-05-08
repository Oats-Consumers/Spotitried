from fastapi import FastAPI
from backend.routers import analytics
from backend.routers import user

app = FastAPI(title="Music Streaming Analytics API")

app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(user.router, prefix="/user", tags=["User"])
@app.get("/")
def root():
    return {"message": "Welcome to the Music Streaming Analytics API"}
