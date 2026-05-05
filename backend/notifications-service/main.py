from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add shared directory to path
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from models import Notification, NotificationCreate
from database import Database
from auth import verify_token
from datetime import datetime
import sqlite3

app = FastAPI(title="Notifications Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotificationsDatabase(Database):
    def init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

db = NotificationsDatabase("data/notifications.db")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notifications-service"}

@app.post("/notifications")
async def create_notification(notification: NotificationCreate):
    with db.get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO notifications (title, message, user_id)
            VALUES (?, ?, ?)
        """, (notification.title, notification.message, notification.user_id))
        conn.commit()
        
        notification_id = cursor.lastrowid
        return {"id": notification_id, "message": "Notification created successfully"}

@app.get("/notifications")
async def get_notifications(current_user_id: int = Depends(verify_token)):
    with db.get_connection() as conn:
        notifications_rows = conn.execute("""
            SELECT id, title, message, user_id, is_read, created_at
            FROM notifications 
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (current_user_id,)).fetchall()
        
        notifications = []
        for row in notifications_rows:
            notifications.append({
                "id": row["id"],
                "title": row["title"],
                "message": row["message"],
                "user_id": row["user_id"],
                "is_read": bool(row["is_read"]),
                "created_at": row["created_at"]
            })
        
        return notifications

@app.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int, current_user_id: int = Depends(verify_token)):
    with db.get_connection() as conn:
        # Check if notification exists and belongs to user
        notification = conn.execute(
            "SELECT * FROM notifications WHERE id = ? AND user_id = ?",
            (notification_id, current_user_id)
        ).fetchone()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        conn.execute(
            "UPDATE notifications SET is_read = TRUE WHERE id = ?",
            (notification_id,)
        )
        conn.commit()
        
        return {"message": "Notification marked as read"}

@app.get("/notifications/unread-count")
async def get_unread_count(current_user_id: int = Depends(verify_token)):
    with db.get_connection() as conn:
        count = conn.execute(
            "SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND is_read = FALSE",
            (current_user_id,)
        ).fetchone()
        
        return {"unread_count": count["count"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)