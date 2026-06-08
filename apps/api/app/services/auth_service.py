from sqlalchemy.orm import Session

from app.core.errors import UnauthorizedError
from app.core.security import create_access_token, verify_password
from app.repositories import user_repo


def login(db: Session, email: str, password: str) -> str:
    """Validates credentials and returns a JWT access token."""
    user = user_repo.get_by_email(db, email)
    if not user or not user.is_active:
        raise UnauthorizedError("Invalid credentials")
    if not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid credentials")
    return create_access_token(subject=str(user.id))
