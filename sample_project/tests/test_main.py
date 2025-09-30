"""
Tests for the TODO API
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app, todos_db


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test"""
    global next_id
    todos_db.clear()
    next_id = 1
    yield
    todos_db.clear()
    next_id = 1


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to TODO API"
    assert "docs" in data
    assert "health" in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_create_todo(client):
    """Test creating a new TODO"""
    todo_data = {"title": "Test TODO", "description": "This is a test TODO"}

    response = client.post("/todos", json=todo_data)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test TODO"
    assert data["description"] == "This is a test TODO"
    assert data["completed"] is False
    assert "created_at" in data
    assert "updated_at" in data


def test_get_todos_empty(client):
    """Test getting todos when list is empty"""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_get_todos(client):
    """Test getting all todos"""
    # Create some todos
    client.post("/todos", json={"title": "TODO 1"})
    client.post("/todos", json={"title": "TODO 2", "description": "Description"})

    response = client.get("/todos")
    assert response.status_code == 200

    todos = response.json()
    assert len(todos) == 2
    assert todos[0]["title"] == "TODO 1"
    assert todos[1]["title"] == "TODO 2"


def test_get_todos_filtered_by_completed(client):
    """Test filtering todos by completion status"""
    # Create todos
    response1 = client.post("/todos", json={"title": "TODO 1"})
    todo1_id = response1.json()["id"]
    client.post("/todos", json={"title": "TODO 2"})

    # Mark first todo as completed
    client.put(f"/todos/{todo1_id}", json={"completed": True})

    # Get only completed todos
    response = client.get("/todos?completed=true")
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["completed"] is True

    # Get only pending todos
    response = client.get("/todos?completed=false")
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["completed"] is False


def test_get_todo_by_id(client):
    """Test getting a specific TODO by ID"""
    # Create a todo
    response = client.post("/todos", json={"title": "Test TODO"})
    todo_id = response.json()["id"]

    # Get it by ID
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test TODO"


def test_get_todo_not_found(client):
    """Test getting a non-existent TODO"""
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_todo(client):
    """Test updating a TODO"""
    # Create a todo
    response = client.post("/todos", json={"title": "Original Title"})
    todo_id = response.json()["id"]

    # Update it
    update_data = {"title": "Updated Title", "description": "New description", "completed": True}
    response = client.put(f"/todos/{todo_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "New description"
    assert data["completed"] is True


def test_update_todo_partial(client):
    """Test partial update of a TODO"""
    # Create a todo
    response = client.post("/todos", json={"title": "Original", "description": "Original desc"})
    todo_id = response.json()["id"]

    # Update only the title
    response = client.put(f"/todos/{todo_id}", json={"title": "New Title"})
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "New Title"
    assert data["description"] == "Original desc"  # Should remain unchanged


def test_update_todo_not_found(client):
    """Test updating a non-existent TODO"""
    response = client.put("/todos/999", json={"title": "New Title"})
    assert response.status_code == 404


def test_delete_todo(client):
    """Test deleting a TODO"""
    # Create a todo
    response = client.post("/todos", json={"title": "To Delete"})
    todo_id = response.json()["id"]

    # Delete it
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]

    # Verify it's gone
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404


def test_delete_todo_not_found(client):
    """Test deleting a non-existent TODO"""
    response = client.delete("/todos/999")
    assert response.status_code == 404


def test_get_stats(client):
    """Test getting TODO statistics"""
    # Initially empty
    response = client.get("/stats")
    stats = response.json()
    assert stats["total"] == 0
    assert stats["completed"] == 0
    assert stats["pending"] == 0
    assert stats["completion_rate"] == "0%"

    # Create some todos
    response1 = client.post("/todos", json={"title": "TODO 1"})
    client.post("/todos", json={"title": "TODO 2"})
    todo1_id = response1.json()["id"]

    # Mark one as completed
    client.put(f"/todos/{todo1_id}", json={"completed": True})

    # Check stats
    response = client.get("/stats")
    stats = response.json()
    assert stats["total"] == 2
    assert stats["completed"] == 1
    assert stats["pending"] == 1
    assert stats["completion_rate"] == "50.0%"


def test_validation_errors(client):
    """Test validation errors"""
    # Empty title
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422

    # Missing title
    response = client.post("/todos", json={"description": "No title"})
    assert response.status_code == 422

    # Title too long
    response = client.post("/todos", json={"title": "x" * 101})
    assert response.status_code == 422
