from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.main import app

client = TestClient(app)

# Mock data
mock_project = {
    "project_id": 1,
    "name": "Test Project",
    "description": "Test",
    "owner_id": 1,
    "created_at": "2025-01-01T00:00:00"
}

def login_user(username: str, password: str):
    login_data = {"username": username, "password": password}
    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]

def test_create_project_end_to_end():
    # User registration
    register_data = {
        "username": "alice",
        "password": "secret123",
    }
    response = client.post("/auth", json=register_data)
    assert response.status_code in [201, 400]

    # User login
    token = login_user("alice", "secret123")

    # Create project
    headers = {"Authorization": f"Bearer {token}"}
    project_data = {"name": "My Project", "description": "Test"}
    response = client.post("/projects", json=project_data, headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Project created"

def test_list_projects_authenticated():
    # User registration
    register_data = {
        "username": "bob",
        "password": "secret123",
    }
    response = client.post("/auth", json=register_data)
    assert response.status_code in [201, 400]

    # User login
    token = login_user("bob", "secret123")

    # List projects
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/projects", headers=headers)

    # Assert
    assert response.status_code == 200
    assert "projects" in response.json()
