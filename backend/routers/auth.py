from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel, EmailStr

from db.database import get_session
from db.models import User
from services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

# Model pomocniczy do logowania
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", response_model=User)
def register(user: User, session: Session = Depends(get_session)):

   # Rejestracja nowego użytkownika - Sprawdza unikalność emaila i haszuje hasło.
 
    return auth_service.register_user(user, session)

@router.post("/login")
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
 
    # Logowanie użytkownika. Zwraca token JWT (Access Token).
    return auth_service.authenticate_user(login_data, session)