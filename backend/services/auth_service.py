from datetime import datetime
import os
from sqlmodel import Session, select
from fastapi import HTTPException, status
from datetime import timedelta
from db.models import User
from utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


class AuthService:
    def register_user(self, user: User, session: Session) -> User:
        statement = select(User).where(User.email == user.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = get_password_hash(user.password)
        user.password = hashed_password

        current_dateTime = datetime.now()
        user.created_at = current_dateTime.strftime("%d.%m.%Y")

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def authenticate_user(self, login_data, session: Session):
        statement = select(User).where(User.email == login_data.email)
        user = session.exec(statement).first()

        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user.online_status = True
        session.add(user)
        session.commit()
        session.refresh(user)

        access_token_expires_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(ACCESS_TOKEN_EXPIRE_MINUTES))
        )

        access_token_expires = timedelta(minutes=access_token_expires_minutes)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    def logout_user(self, user: User, session: Session):
        user.online_status = False
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"message": "Successfully logged out"}
