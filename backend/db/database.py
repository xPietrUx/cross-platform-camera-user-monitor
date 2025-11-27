from sqlmodel import SQLModel, create_engine, Session

# Nazwa pliku bazy danych
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
