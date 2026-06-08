# FastAPI dependencies for authentication and role enforcement.
# Use get_current_user as a dependency on any protected route.
# Use require_role("admin") to enforce minimum role level.
import uuid
from typing import Annotated

from fastapi import Depends, Header
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.errors import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole

# Role hierarchy — higher index means more permissions
_ROLE_ORDER = [UserRole.viewer, UserRole.engineer, UserRole.admin]


def _get_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid Authorization header")
    return authorization.removeprefix("Bearer ").strip()


def get_current_user(
    token: Annotated[str, Depends(_get_token)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError()
    except JWTError:
        raise UnauthorizedError("Invalid or expired token")

    user = db.get(User, uuid.UUID(user_id))
    if not user or not user.is_active:
        raise UnauthorizedError("User not found or inactive")
    return user


def require_role(minimum_role: UserRole):
    """Returns a dependency that enforces a minimum role level."""
    def _check(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if _ROLE_ORDER.index(current_user.role) < _ROLE_ORDER.index(minimum_role):
            raise ForbiddenError(f"Requires role: {minimum_role.value}")
        return current_user
    return _check


# Convenient pre-built dependencies
CurrentUser = Annotated[User, Depends(get_current_user)]
RequireEngineer = Annotated[User, Depends(require_role(UserRole.engineer))]
RequireAdmin = Annotated[User, Depends(require_role(UserRole.admin))]
