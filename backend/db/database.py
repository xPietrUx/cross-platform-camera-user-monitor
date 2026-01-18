import sys
import os
import shutil
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session

# Ustalanie ścieżki do bazy danych
if getattr(sys, "frozen", False):
    app_data = os.getenv("APPDATA")
    if not app_data:
        app_data = os.path.expanduser("~")

    app_dir = Path(app_data) / "CrossPlatformCamera"
    app_dir.mkdir(parents=True, exist_ok=True)
    sqlite_file_name = app_dir / "database.db"

    if not sqlite_file_name.exists():
        bundled_db = Path(sys.executable).parent / "database.db"

        if bundled_db.exists():
            try:
                print(
                    f"[INIT] Kopiowanie bazy startowej z {bundled_db} do {sqlite_file_name}"
                )
                shutil.copy2(bundled_db, sqlite_file_name)
            except Exception as e:
                print(f"[ERROR] Nie udało się skopiować bazy startowej: {e}")
else:
    sqlite_file_name = "database.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Tworzenie tabel w bazie danych na podstawie modeli"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency do wstrzykiwania sesji bazy danych w endpoint"""
    with Session(engine) as session:
        yield session
