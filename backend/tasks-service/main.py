from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

from models import TaskCreate, TaskUpdate
from database import Database
from auth import verify_token
from datetime import datetime

app = FastAPI(title="Tasks Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://users-service:8002")
NOTIFICATIONS_SERVICE_URL = os.getenv("NOTIFICATIONS_SERVICE_URL", "http://notifications-service:8003")

class TasksDatabase(Database):
    def init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    priority TEXT DEFAULT 'medium',
                    assigned_to INTEGER,
                    due_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by INTEGER NOT NULL
                )
            """)
            conn.commit()

db = TasksDatabase("data/tasks.db")

async def get_user_info(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USERS_SERVICE_URL}/users/{user_id}")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

async def send_notification(user_id: int, title: str, message: str):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                f"{NOTIFICATIONS_SERVICE_URL}/notifications",
                json={"user_id": user_id, "title": title, "message": message}
            )
        except:
            pass

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tasks-service"}

@app.get("/tasks")
async def get_tasks(current_user_id: int = Depends(verify_token)):
    with db.get_connection() as conn:
        tasks_rows = conn.execute("""
            SELECT id, title, description, status, priority, assigned_to, 
                   due_date, created_at, updated_at, created_by
            FROM tasks 
            WHERE created_by = ? OR assigned_to = ?
            ORDER BY created_at DESC
        """, (current_user_id, current_user_id)).fetchall()
        
        tasks = []
        for row in tasks_rows:
            created_by_info = await get_user_info(row["created_by"])
            assigned_user_info = None
            if row["assigned_to"]:
                assigned_user_info = await get_user_info(row["assigned_to"])
            
            tasks.append({
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "status": row["status"],
                "priority": row["priority"],
                "assigned_to": row["assigned_to"],
                "assigned_user_name": assigned_user_info["name"] if assigned_user_info else None,
                "due_date": row["due_date"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "created_by": row["created_by"],
                "created_by_name": created_by_info["name"] if created_by_info else "Unknown"
            })
        
        return tasks

@app.post("/tasks")
async def create_task(task: TaskCreate, current_user_id: int = Depends(verify_token)):
    with db.get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO tasks (title, description, priority, assigned_to, due_date, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (task.title, task.description, task.priority, task.assigned_to, task.due_date, current_user_id))
        conn.commit()

        task_id = cursor.lastrowid

        if task.assigned_to and task.assigned_to != current_user_id:
            await send_notification(
                task.assigned_to,
                "Nova tarefa atribuída",
                f"Uma nova tarefa '{task.title}' foi atribuída para você."
            )

        task_row = conn.execute("""
            SELECT * FROM tasks WHERE id = ?
        """, (task_id,)).fetchone()

        created_by_info = await get_user_info(task_row["created_by"])
        assigned_user_info = await get_user_info(task_row["assigned_to"]) if task_row["assigned_to"] else None

        return {
            "id": task_row["id"],
            "title": task_row["title"],
            "description": task_row["description"],
            "status": task_row["status"],
            "priority": task_row["priority"],
            "assigned_to": task_row["assigned_to"],
            "assigned_user_name": assigned_user_info["name"] if assigned_user_info else None,
            "due_date": task_row["due_date"],
            "created_at": task_row["created_at"],
            "updated_at": task_row["updated_at"],
            "created_by": task_row["created_by"],
            "created_by_name": created_by_info["name"] if created_by_info else "Unknown"
        }

def traduzir_status(status: str) -> str:
    traducoes = {
        "pending": "PENDENTE",
        "in_progress": "EM PROGRESSO",
        "completed": "CONCLUÍDA",
        "cancelled": "CANCELADA"
    }
    return traducoes.get(status.lower(), status)

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate, current_user_id: int = Depends(verify_token)):
    with db.get_connection() as conn:
        existing_task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")

        update_fields = []
        update_values = []

        if task_update.title is not None:
            update_fields.append("title = ?")
            update_values.append(task_update.title)
        if task_update.description is not None:
            update_fields.append("description = ?")
            update_values.append(task_update.description)
        if task_update.status is not None:
            update_fields.append("status = ?")
            update_values.append(task_update.status)
        if task_update.priority is not None:
            update_fields.append("priority = ?")
            update_values.append(task_update.priority)
        if task_update.assigned_to is not None:
            update_fields.append("assigned_to = ?")
            update_values.append(task_update.assigned_to)
        if task_update.due_date is not None:
            update_fields.append("due_date = ?")
            update_values.append(task_update.due_date)

        if update_fields:
            update_fields.append("updated_at = ?")
            update_values.append(datetime.now().isoformat())
            update_values.append(task_id)

            conn.execute(
                f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?",
                update_values
            )
            conn.commit()

            updated_task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

            if task_update.status and task_update.status.lower() != existing_task["status"].lower():
                if updated_task["assigned_to"]:
                    status_pt = traduzir_status(task_update.status)
                    print(f"Enviando notificação: tarefa '{updated_task['title']}', status {status_pt}")
                    await send_notification(
                        updated_task["assigned_to"],
                        "Status da tarefa alterado",
                        f"A tarefa '{updated_task['title']}' teve seu status alterado para {status_pt}."
                    )

        else:
            updated_task = existing_task

        created_by_info = await get_user_info(updated_task["created_by"])
        assigned_user_info = await get_user_info(updated_task["assigned_to"]) if updated_task["assigned_to"] else None

        return {
            "id": updated_task["id"],
            "title": updated_task["title"],
            "description": updated_task["description"],
            "status": updated_task["status"],
            "priority": updated_task["priority"],
            "assigned_to": updated_task["assigned_to"],
            "assigned_user_name": assigned_user_info["name"] if assigned_user_info else None,
            "due_date": updated_task["due_date"],
            "created_at": updated_task["created_at"],
            "updated_at": updated_task["updated_at"],
            "created_by": updated_task["created_by"],
            "created_by_name": created_by_info["name"] if created_by_info else "Unknown"
        }

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user_id: int = Depends(verify_token)):
    with db.get_connection() as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

        return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)