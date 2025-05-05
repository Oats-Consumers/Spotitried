from fastapi import FastAPI
from backend.routers import analytics

app = FastAPI(title="Music Streaming Analytics API")

app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {"message": "Welcome to the Music Streaming Analytics API"}
