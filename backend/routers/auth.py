from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel, EmailStr

from db.database import get_session
from dependencies import get_current_user
from db.models import User
from services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", response_model=User)
def register(user: User, session: Session = Depends(get_session)):

    return auth_service.register_user(user, session)


@router.post("/login")
def login(login_data: LoginRequest, session: Session = Depends(get_session)):

    return auth_service.authenticate_user(login_data, session)


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return auth_service.logout_user(current_user, session)
