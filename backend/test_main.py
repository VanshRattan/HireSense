from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import os

# Setup in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to HireSense API"}

def test_start_session():
    # Test creating a session. For this we need a user ideally, but if foreign key is not strictly enforced in sqlite:
    response = client.post("/sessions/start", json={"user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["user_id"] == 1
    
    # Store session id for teardown/later tests if needed
    global session_id 
    session_id = data["id"]
