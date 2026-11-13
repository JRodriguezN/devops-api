from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="DevOps API",
    description="API for github Actions CI/CD hands-on",
    version="1.0.0"
)

tasks = []
task_id_counter = 1

class Task(BaseModel):
    title:str
    description: str = ""

@app.get("/")
def root():
    return {
        "message":"Welcome to DevOps API",
        "version":"1.0.0"
    } 

@app.get("/health")
def health_check():
    return {
        "status" :"healthy"
    }
    
@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global task_id_counter

    new_task = {
        "id" : task_id_counter,
        "title" : task.title,
        "description": task.description,
        "completed" : False 
    }
    
    tasks.append(new_task)
    task_id_counter += 1
    
    return new_task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    raise HTTPException(
        status_code=404,
        detail="Task Not found"  
    )