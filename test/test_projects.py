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
    headers = {"Authorization": f"Bearer {token}"}

    # Create project
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
    headers = {"Authorization": f"Bearer {token}"}

    # List projects
    response = client.get("/projects", headers=headers)

    # Assert
    assert response.status_code == 200
    assert "projects" in response.json()

def test_get_project_info_authenticated():
    # User registration
    register_data = {
        "username": "adam",
        "password": "321terces",
    }
    response = client.post("/auth", json=register_data)
    assert response.status_code in [201, 400]

    # User login
    token = login_user("adam", "321terces")
    headers = {"Authorization": f"Bearer {token}"}

    # Project create
    project_data = {"name": "Test Project", "description": "For testing"}
    response = client.post("/projects", json=project_data, headers=headers)
    assert response.status_code == 200
    created_project = response.json()["project"]
    project_id = created_project["project_id"]

    # Get project info
    response = client.get(f"/projects/{project_id}/info", headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "project" in data
    assert data["project"]["project_id"] == project_id
    assert data["project"]["name"] == "Test Project"

def test_update_project_info():
    # User registration
    register_data = {
        "username": "charlie",
        "password": "very$3CR3T123",
    }
    response = client.post("/auth", json=register_data)
    assert response.status_code in [201, 400]

    # User login
    token = login_user("charlie", "very$3CR3T123")
    headers = {"Authorization": f"Bearer {token}"}

    # Project create
    project_data = {"name": "Test Project", "description": "For testing"}
    response = client.post("/projects", json=project_data, headers=headers)
    assert response.status_code == 200
    created_project = response.json()["project"]
    project_id = created_project["project_id"]

    # Project update
    update_data = {"name": "New Name", "description": "New description"}
    response = client.put(f"/projects/{project_id}/info", json=update_data, headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "updated" in data
    updated = data["updated"]
    assert updated["project_id"] == project_id
    assert updated["name"] == "New Name"
    assert updated["description"] == "New description"

def test_delete_project_owner():
    # User registration
    register_data = {
        "username": "eve",
        "password": "loremipsum",
    }
    response = client.post("/auth", json=register_data)
    assert response.status_code in [201, 400]

    # User login
    token = login_user("eve", "loremipsum")
    headers = {"Authorization": f"Bearer {token}"}

    # Project create
    project_data = {"name": "Test Project", "description": "For testing"}
    response = client.post("/projects", json=project_data, headers=headers)
    assert response.status_code == 200
    created_project = response.json()["project"]
    project_id = created_project["project_id"]

    # Project delete
    response = client.delete(f"/projects/{project_id}", headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Project deleted"

    # Verify project no longer exists
    response = client.get(f"/projects/{project_id}/info", headers=headers)
    assert response.status_code == 404