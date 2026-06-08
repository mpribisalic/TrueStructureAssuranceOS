from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserMeResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    token = auth_service.login(db, data.email, data.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserMeResponse)
def me(current_user: CurrentUser):
    return current_user


@router.post("/logout")
def logout():
    # JWT is stateless — logout is handled client-side by discarding the token.
    # This endpoint exists for API completeness and future token blacklist support.
    return {"message": "Logged out"}
