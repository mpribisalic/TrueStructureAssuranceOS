"""Seed script — creates demo organization, user and project.
Run with: uv run python scripts/seed_demo.py
Idempotent: safe to run multiple times (skips existing records).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import hash_password
from app.db.base import import_all_models
from app.db.session import SessionLocal
from app.models.organization import Organization
from app.models.project import CriticalityLevel, Industry, Project
from app.models.user import User, UserRole

import_all_models()

DEMO_ORG_NAME = "Assurance OS Demo"
DEMO_EMAIL = "demo@assuranceos.dev"
DEMO_PASSWORD = "demo1234"
DEMO_PROJECT_NAME = "Autonomous Reconnaissance Sensor Platform"


def seed():
    db = SessionLocal()
    try:
        # Organization
        org = db.query(Organization).filter_by(name=DEMO_ORG_NAME).first()
        if not org:
            org = Organization(name=DEMO_ORG_NAME, industry="defense")
            db.add(org)
            db.flush()
            print(f"Created organization: {org.name}")
        else:
            print(f"Organization exists: {org.name}")

        # Demo admin user
        user = db.query(User).filter_by(email=DEMO_EMAIL).first()
        if not user:
            user = User(
                organization_id=org.id,
                email=DEMO_EMAIL,
                name="Demo User",
                password_hash=hash_password(DEMO_PASSWORD),
                role=UserRole.admin,
            )
            db.add(user)
            db.flush()
            print(f"Created user: {user.email} / {DEMO_PASSWORD}")
        else:
            print(f"User exists: {user.email}")

        # Demo project
        project = db.query(Project).filter_by(name=DEMO_PROJECT_NAME).first()
        if not project:
            project = Project(
                organization_id=org.id,
                name=DEMO_PROJECT_NAME,
                description=(
                    "A dual-use autonomous sensor platform used for reconnaissance, "
                    "remote inspection and critical infrastructure monitoring."
                ),
                industry=Industry.defense,
                system_type="autonomous_sensor",
                criticality_level=CriticalityLevel.mission_critical,
            )
            db.add(project)
            db.flush()
            print(f"Created project: {project.name}")
        else:
            print(f"Project exists: {project.name}")

        db.commit()
        print("\nSeed complete.")
        print(f"  Login: {DEMO_EMAIL}")
        print(f"  Password: {DEMO_PASSWORD}")
        print(f"  Project: {DEMO_PROJECT_NAME}")
    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
