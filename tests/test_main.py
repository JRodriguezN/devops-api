from fastapi.testclient import TestClient
from app.main import app, tasks
import app.main as main
client = TestClient(app)



def setup_function():
    tasks.clear()
    main.task_id_counter = 1
def test_root():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to DevOps API"
    
def test_health():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title":"Learn GitHub Actions",
            "description":"Build CI/CD pipeline"
        }
    )
    
    assert response.status_code == 201
    assert response.json()["title"] == "Learn GitHub Actions"
    assert response.json()["description"] == "Build CI/CD pipeline"
    

def test_get_tasks():
    client.post(
        "/tasks",
        json={
            "title":"First Task"
        }
    )
    response = client.get("/tasks")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    
def test_get_task_by_id():
    client.post(
        "/tasks",
        json={
            "title":"First task",
            "description":"First task description"
        }
    )
    
    client.post(
        "/tasks",
        json={
            "title":"Second task",
            "description":"Second task description"
        }
    )
    
    response = client.get("/tasks/1")
    
    assert response.status_code == 200
    assert response.json()["title"] == "First task"
    
    response = client.get("/tasks/2")
        
    assert response.status_code == 200
    assert response.json()["title"] == "Second task"
        
        
def test_task_not_found():
    response = client.get("/tasks/999")
    
    assert response.status_code == 404
    
    