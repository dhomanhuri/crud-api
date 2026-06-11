from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.responses import FileResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uuid
import os
import secrets

app = FastAPI(title="CRUD User API", version="1.0.0")

# --- API Key Config ---
API_KEY = os.environ.get("API_KEY", "secret-api-key-12345")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or not secrets.compare_digest(api_key, API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key

# --- Model ---
class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserOut(User):
    id: str

# --- Dummy Data ---
db: dict[str, UserOut] = {
    "1": UserOut(id="1", name="Ilyas", email="ilyas@example.com", age=25),
    "2": UserOut(id="2", name="Budi", email="budi@example.com", age=30),
    "3": UserOut(id="3", name="Siti", email="siti@example.com", age=22),
}

# --- Static Files ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Routes ---
@app.get("/")
def dashboard():
    return FileResponse("static/index.html")

@app.get("/api")
def root():
    return {"message": "CRUD User API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users", response_model=list[UserOut], dependencies=[Depends(verify_api_key)])
def get_all_users():
    return list(db.values())

@app.get("/users/{user_id}", response_model=UserOut, dependencies=[Depends(verify_api_key)])
def get_user(user_id: str):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return db[user_id]

@app.post("/users", response_model=UserOut, status_code=201, dependencies=[Depends(verify_api_key)])
def create_user(user: User):
    new_id = str(uuid.uuid4())[:8]
    new_user = UserOut(id=new_id, **user.model_dump())
    db[new_id] = new_user
    return new_user

@app.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(verify_api_key)])
def update_user(user_id: str, user: User):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    updated = UserOut(id=user_id, **user.model_dump())
    db[user_id] = updated
    return updated

@app.delete("/users/{user_id}", dependencies=[Depends(verify_api_key)])
def delete_user(user_id: str):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    del db[user_id]
    return {"message": f"User {user_id} deleted"}
