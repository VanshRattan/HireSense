from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HireSense API")

from database import engine
import models
models.Base.metadata.create_all(bind=engine)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import sessions

app.include_router(sessions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to HireSense API"}
