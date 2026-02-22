from typing import Annotated
from fastapi import FastAPI , Depends , HTTPException
from . import models , schemas , crud 
from .db import engine , open_db
from sqlalchemy.orm import Session
from .auth import verify_pass , create_access_token , get_current_user

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task manager")

# Reusable dependency types
db_dep = Annotated[Session, Depends(open_db)]
user_dep = Annotated[dict, Depends(get_current_user)]

# --- USER ENDPOINTS ---
@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
def create_user(user : schemas.CreateUser , db : db_dep):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud.get_user_by_contact(db, contact_num=user.contact_num):
        raise HTTPException(status_code=400, detail="Contact number already registered")
    return crud.create_user(db , user)

@app.get("/users/", response_model=list[schemas.UserResponse], tags=["Users"])
def get_all_users(db: db_dep, current_user: user_dep):
    return crud.get_user(db)

# --- TASK ENDPOINTS (Protected) ---

# STEP 1: Update Route
@app.get("/tasks/me", response_model=list[schemas.TaskResponse], tags=["Tasks"])
def get_my_tasks(db: db_dep, current_user: user_dep):
    user_id = current_user["user_id"]
    return crud.get_task_by_user(db , user_id)

# STEP 2: Update Create Task
@app.post("/tasks", response_model=schemas.TaskResponse, tags=["Tasks"])
def create_task(
    task : schemas.CreateTask , 
    db: db_dep, 
    current_user: user_dep
):
    user_id = current_user["user_id"]
    # No need to check if user exists, as get_current_user already ensures a valid user.
    return crud.create_task(db , task , user_id)

# STEP 3: Remove user_id from update/delete if possible
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task_status(
    task_id:int , 
    completed:bool , 
    db: db_dep, 
    current_user: user_dep
):
    user_id = current_user["user_id"]
    task = crud.update_task(db , task_id , completed, user_id)
    if not task : 
        raise HTTPException(status_code=404 , detail="Task not found")
    return task 

@app.delete("/task/{task_id}", tags=["Tasks"])
def delete_task_by_id(task_id:int , db: db_dep, current_user: user_dep):
    user_id = current_user["user_id"]
    task = crud.delete_task(db , task_id, user_id)
    if not task : 
        raise HTTPException(status_code=404 , detail="Task not found")
    return {"message":"Task deleted successfully"}

# --- AUTHENTICATION ---
@app.post("/login", response_model=schemas.Token, tags=["Authentication"])
def login(email:str , password : str ,db : db_dep):
    user = crud.get_user_by_email(db, email)
    if not user or not verify_pass(password, user.password): 
        raise HTTPException(status_code=401 , detail="Invalid email or password")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
