import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / "JWT" / ".env"
load_dotenv(dotenv_path=ENV_PATH)
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(f"Nie znaleziono SECRET_KEY w pliku: {ENV_PATH}")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Konfiguracja Passlib (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Weryfikuje czy podane hasło pasuje do hasha
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Generuje hash hasła
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # Tworzy token JWT z czasem wygasania
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt