from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
import sys
import os
from fastapi.middleware.cors import CORSMiddleware


# Dodanie ścieżki do folderu nadrzędnego ('backend'), aby znaleźć moduł 'services'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import create_db_and_tables, get_session
from db.models import User
from routers import video


# Uruchomienie bazy danych
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI()

# Video Route
app.include_router(video.router, prefix="/video", tags=["Video"])

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
    # Strona powitalna API
    return {"message": "Witaj w API do monitorowania użytkownika."}


# --- Użytkownicy ---
# Dodanie bazy i użytkowników
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Podgląd użytkowników
@app.get("/users/", response_model=List[User])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@app.post("/login")
def login():
    # Logowanie
    return {"message": "Zalogowano pomyślnie", "token": "fake-jwt-token"}


@app.post("/register")
def register():
    # Rejestracja
    return {"message": "Użytkownik zarejestrowany pomyślnie"}


@app.post("/logout")
def logout():
    # Wylogowanie
    return {"message": "Wylogowano pomyślnie"}


@app.get("/users/me")
def get_current_user():
    # Pobiera dane zalogowanego użytkownika.
    return {"username": "testuser", "email": "test@example.com"}


@app.put("/users/me")
def update_current_user():
    # Aktualizuje dane zalogowanego użytkownika.
    return {"message": "Dane użytkownika zaktualizowane"}


# --- Śledzenie ---


@app.post("/tracking/session/start")
def start_tracking_session():
    # Rozpoczyna nową sesję śledzenia aktywności.
    return {"message": "Sesja śledzenia rozpoczęta", "session_id": "session123"}


@app.post("/tracking/session/stop")
def stop_tracking_session():
    # Zatrzymuje bieżącą sesję śledzenia.
    return {"message": "Sesja śledzenia zakończona"}


@app.get("/tracking/sessions", response_model=List[dict])
def get_tracking_sessions():
    # Pobiera listę historycznych sesji śledzenia.
    return [
        {"session_id": "session123", "duration": 3600},
        {"session_id": "session456", "duration": 1800},
    ]


@app.get("/tracking/sessions/{session_id}")
def get_session_details(session_id: str):
    # Pobiera szczegółowe dane dla konkretnej sesji śledzenia.
    return {"session_id": session_id, "details": "Szczegółowe dane sesji."}


# --- Analiza na żywo ---


@app.get("/ws/live/events")
def live_events_placeholder():

    return {"message": "Ten endpoint będzie w przyszłości wysyłał zdarzenia na żywo."}


# --- Raporty ---


@app.get("/reports/summary")
def get_summary_report():
    # Zwraca podsumowanie aktywności użytkownika.
    return {"summary": "Podsumowanie aktywności z ostatniego tygodnia."}


@app.post("/reports")
def generate_report():
    # Inicjuje generowanie nowego raportu.
    return {"message": "Generowanie raportu rozpoczęte", "report_id": "report-xyz"}


# --- Ustawienia ---


@app.get("/settings")
def get_settings():
    # Pobiera aktualne ustawienia aplikacji dla użytkownika.
    return {"notifications": True, "detection_sensitivity": "high"}


@app.put("/settings")
def update_settings():
    # Aktualizuje ustawienia aplikacji.
    return {"message": "Ustawienia zaktualizowane"}
