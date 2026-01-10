import sys
import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session

# Ustalanie ścieżki do bazy danych
if getattr(sys, "frozen", False):
    # Jeśli aplikacja jest zbudowana (PyInstaller), zapisz bazę w AppData
    # Windows: C:\Users\User\AppData\Roaming\CrossPlatformCamera
    app_data = os.getenv("APPDATA")
    if not app_data:
        app_data = os.path.expanduser("~")

    app_dir = Path(app_data) / "CrossPlatformCamera"
    app_dir.mkdir(parents=True, exist_ok=True)
    sqlite_file_name = app_dir / "database.db"
else:
    # W trybie developerskim zapisz w folderze projektu
    sqlite_file_name = "database.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False jest potrzebne dla SQLite w FastAPI
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Tworzenie tabel w bazie danych na podstawie modeli"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency do wstrzykiwania sesji bazy danych w endpoint"""
    with Session(engine) as session:
        yield session
