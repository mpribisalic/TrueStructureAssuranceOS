"""Tests for database connectivity and schema correctness — Faza 1 acceptance criterion."""
from sqlalchemy import inspect, text


def test_database_connection(db):
    result = db.execute(text("SELECT 1")).scalar()
    assert result == 1


def test_all_tables_exist(db):
    """Verify all 14 domain tables were created by the migration."""
    inspector = inspect(db.bind)
    tables = set(inspector.get_table_names())
    required = {
        "organizations", "users", "projects",
        "documents", "requirements", "test_cases",
        "test_runs", "evidence", "trace_links",
        "gaps", "readiness_scores", "reports",
        "audit_events",
    }
    missing = required - tables
    assert not missing, f"Missing tables: {missing}"
