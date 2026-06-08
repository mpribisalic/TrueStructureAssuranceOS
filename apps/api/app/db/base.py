# Base class for all SQLAlchemy ORM models.
# Importing this module (not the models themselves) in alembic/env.py
# ensures Alembic can discover all tables for autogenerate.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here so Alembic sees them when generating migrations.
# Add a new import line each time a new model module is created.
# ruff: noqa: F401 (imports used by Alembic, not directly)
def import_all_models() -> None:
    from app.models import audit, document, evidence, gap, organization, project  # noqa: F401
    from app.models import readiness, report, requirement, test_case, test_run  # noqa: F401
    from app.models import trace_link, user  # noqa: F401
    from app.models import mission_impact  # noqa: F401
    from app.models import confidence_score  # noqa: F401
    from app.models import standards  # noqa: F401
