from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import create_db_and_tables, get_session
from db.models import User
from routers import video, auth
from dependencies import get_current_user
from services import video_processor

# Konfiguracja JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    if video_processor.global_camera and video_processor.global_camera.isOpened():
        video_processor.global_camera.release()
        print("Kamera została zwolniona")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Witaj w API do monitorowania użytkownika."}


# --- Użytkownicy ---


# Podgląd użytkowników
@app.get("/users/", response_model=List[User])
def read_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    users = session.exec(select(User)).all()
    return users


@app.get("/users/me", response_model=User)
def get_current_user_endpoint(current_user: User = Depends(get_current_user)):

    return current_user


@app.put("/users/me")
def update_current_user(current_user: User = Depends(get_current_user)):
    return {"message": f"Dane użytkownika {current_user.email} zaktualizowane"}


# Rejestracja routerów
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(video.router, prefix="/video", tags=["video"])
