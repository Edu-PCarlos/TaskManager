from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add shared directory to path
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from models import User, UserCreate, LoginRequest, Token
from database import Database
from auth import get_password_hash, verify_password, create_access_token, verify_token
from datetime import datetime, timedelta
import sqlite3

app = FastAPI(title="Users Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UsersDatabase(Database):
    def init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

db = UsersDatabase("data/users.db")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "users-service"}

@app.post("/users/register")
async def register_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    
    with db.get_connection() as conn:
        try:
            cursor = conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (user.name, user.email, hashed_password)
            )
            conn.commit()
            
            user_id = cursor.lastrowid
            return {"id": user_id, "name": user.name, "email": user.email, "message": "User created successfully"}
            
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

@app.post("/users/login")
async def login_user(login_data: LoginRequest):
    with db.get_connection() as conn:
        user_row = conn.execute(
            "SELECT id, name, email, password_hash FROM users WHERE email = ?",
            (login_data.email,)
        ).fetchone()

        # Usar senha dummy para evitar ataque de tempo (proteção adicional)
        fake_hash = get_password_hash("fake_password")

        if not user_row:
            verify_password("fake_password", fake_hash)  # Dummy verification
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        if not verify_password(login_data.password, user_row["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user_row["id"])}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_row["id"],
                "name": user_row["name"],
                "email": user_row["email"]
            }
        }

@app.get("/users")
async def get_users(current_user_id: int = Depends(verify_token)):
    with db.get_connection() as conn:
        users_rows = conn.execute(
            "SELECT id, name, email, created_at FROM users ORDER BY name"
        ).fetchall()
        
        users = []
        for row in users_rows:
            users.append({
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "created_at": row["created_at"]
            })
        
        return users

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    with db.get_connection() as conn:
        user_row = conn.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        
        if not user_row:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user_row["id"],
            "name": user_row["name"],
            "email": user_row["email"],
            "created_at": user_row["created_at"]
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)