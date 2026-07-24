from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, glob

# Dynamically inject ffmpeg into PATH if installed via winget to prevent restart requirements
ffmpeg_path = glob.glob(os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Microsoft', 'WinGet', 'Packages', '**', 'ffmpeg.exe'), recursive=True)
if ffmpeg_path:
    os.environ['PATH'] += os.pathsep + os.path.dirname(ffmpeg_path[0])

app = FastAPI(title="HireSense API")
# Backend API Key Reload Trigger 2

from database import engine
import models
models.Base.metadata.create_all(bind=engine)

# Configure CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import sessions

app.include_router(sessions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to HireSense API"}
