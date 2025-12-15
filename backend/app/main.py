from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Query  # Dodaj Query
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from jose import JWTError, jwt
import sys
import os
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import create_db_and_tables, get_session
from db.models import User
from routers import video, auth

# Konfiguracja JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Auth do Endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_token_from_header_or_query(
    header_token: str = Depends(oauth2_scheme),
    query_token: str = Query(None, alias="token"),
):
    if header_token:
        return header_token
    if query_token:
        return query_token

    # Jeśli brak obu, rzucamy błąd
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Brak tokena uwierzytelniającego",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    token: str = Depends(get_token_from_header_or_query),  # Używamy nowej funkcji
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nieprawidłowe dane uwierzytelniające",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Dekodowanie i weryfikacja podpisu tokena
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Pobranie użytkownika z bazy
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise credentials_exception

    return user


# Routery

# Zabezpieczenie całego routera Video
app.include_router(
    video.router,
    prefix="/video",
    tags=["Video"],
    dependencies=[Depends(get_current_user)],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Poprawna komunikacja z Frontend
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


# Podgląd użytkowników - wymaga zalogowania
@app.get("/users/", response_model=List[User])
def read_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    users = session.exec(select(User)).all()
    return users


@app.get("/users/me", response_model=User)
def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    # Zwraca dane użytkownika wyciągnięte z tokena
    return current_user


@app.put("/users/me")
def update_current_user(current_user: User = Depends(get_current_user)):
    return {"message": f"Dane użytkownika {current_user.email} zaktualizowane"}
