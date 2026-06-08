"""Tests for project CRUD endpoints — Faza 2 acceptance criterion."""


def test_create_project(client, auth_headers):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "My Test Project",
            "industry": "defense",
            "criticality_level": "high",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Test Project"
    assert data["industry"] == "defense"
    assert "id" in data


def test_list_projects(client, auth_headers, demo_project):
    response = client.get("/api/v1/projects", headers=auth_headers)
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) >= 1
    names = [p["name"] for p in projects]
    assert "Test Project" in names


def test_get_project(client, auth_headers, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"


def test_get_project_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/projects/{fake_id}", headers=auth_headers)
    assert response.status_code == 404


def test_update_project(client, auth_headers, demo_project):
    response = client.patch(
        f"/api/v1/projects/{demo_project.id}",
        json={"name": "Updated Project Name"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Project Name"


def test_delete_project(client, auth_headers, demo_project):
    response = client.delete(
        f"/api/v1/projects/{demo_project.id}",
        headers=auth_headers,
    )
    assert response.status_code == 204


def test_project_requires_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}")
    assert response.status_code == 401
