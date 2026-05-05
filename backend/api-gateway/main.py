from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from typing import List

app = FastAPI(title="Task Manager API Gateway")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
TASKS_SERVICE_URL = os.getenv("TASKS_SERVICE_URL", "http://localhost:8001")
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:8002")
NOTIFICATIONS_SERVICE_URL = os.getenv("NOTIFICATIONS_SERVICE_URL", "http://localhost:8003")

async def forward_request(service_url: str, path: str, method: str = "GET", json_data=None, headers=None):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=f"{service_url}{path}",
                json=json_data,
                headers=headers,
                timeout=30.0
            )
            return response
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-gateway"}

# User routes
@app.post("/api/users/register")
async def register_user(user_data: dict):
    response = await forward_request(USERS_SERVICE_URL, "/users/register", "POST", user_data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.post("/api/users/login")
async def login_user(login_data: dict):
    response = await forward_request(USERS_SERVICE_URL, "/users/login", "POST", login_data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.get("/api/users")
async def get_users(authorization: str = Header(None)):
    headers = {"Authorization": authorization} if authorization else None
    response = await forward_request(USERS_SERVICE_URL, "/users", "GET", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

# Task routes
@app.get("/api/tasks")
async def get_tasks(authorization: str = Header(...)):
    headers = {"Authorization": authorization} if authorization else None
    response = await forward_request(TASKS_SERVICE_URL, "/tasks", "GET", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.post("/api/tasks")
async def create_task(task_data: dict, authorization: str = Header(None)):
    headers = {"Authorization": authorization} if authorization else None
    response = await forward_request(TASKS_SERVICE_URL, "/tasks", "POST", task_data, headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, task_data: dict, authorization: str = Header(None)):
    headers = {"Authorization": authorization} if authorization else None
    response = await forward_request(TASKS_SERVICE_URL, f"/tasks/{task_id}", "PUT", task_data, headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, authorization: str = Header(None)):
    headers = {"Authorization": authorization} if authorization else None
    response = await forward_request(TASKS_SERVICE_URL, f"/tasks/{task_id}", "DELETE", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

# Notification routes
@app.get("/api/notifications")
async def get_notifications(authorization: str = Header(None)):
    headers = {"Authorization": authorization} if authorization else None
    response = await forward_request(NOTIFICATIONS_SERVICE_URL, "/notifications", "GET", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.put("/api/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int, authorization: str = Header(None)):
    headers = {"Authorization": authorization} if authorization else None
    response = await forward_request(NOTIFICATIONS_SERVICE_URL, f"/notifications/{notification_id}/read", "PUT", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
