from pyexpat.errors import messages
from typing import Annotated , Optional

from alembic.command import history
from fastapi import FastAPI , Depends , HTTPException
from starlette.requests import Request

from . import models , schemas , crud
from .db import engine , open_db
from sqlalchemy.orm import Session
from .auth import verify_pass , create_access_token , get_current_user
from slowapi import Limiter , _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from .config import GROQ_API_KEY
from groq import Groq

limiter =Limiter(get_remote_address)
groq_client = Groq(api_key=GROQ_API_KEY)
app = FastAPI(title="Task manager")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

# Reusable dependency types
db_dep = Annotated[Session, Depends(open_db)]
user_dep = Annotated[dict, Depends(get_current_user)]

# --- USER ENDPOINTS ---
@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
@limiter.limit("10/minute")
def create_user(request : Request , user : schemas.CreateUser , db : db_dep):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud.get_user_by_contact(db, contact_num=user.contact_num):
        raise HTTPException(status_code=400, detail="Contact number already registered")
    return crud.create_user(db , user)

@app.get("/users/", response_model=list[schemas.UserResponse], tags=["Users"])
@limiter.limit("10/minute")
def get_all_users(request : Request ,db: db_dep, current_user: user_dep):
    return crud.get_user(db)

# --- TASK ENDPOINTS (Protected) ---

# STEP 1: Update Route
@app.get("/tasks/me", response_model=list[schemas.TaskResponse], tags=["Tasks"])
@limiter.limit("10/minute")
def get_my_tasks(request : Request , db: db_dep , current_user : user_dep, skip : int = 0 , limit : int = 10 , completed : Optional[bool] = None , sort : str = "created_at" , order : str = "desc"):
    user_id = current_user["user_id"]
    return crud.get_task_by_user(db , user_id, skip, limit, completed)

# STEP 2: Update Create Task
@app.post("/tasks", response_model=schemas.TaskResponse, tags=["Tasks"])
@limiter.limit("10/minute")
def create_task(
    request : Request ,
    task : schemas.CreateTask , 
    db: db_dep, 
    current_user: user_dep
):
    user_id = current_user["user_id"]
    # No need to check if user exists, as get_current_user already ensures a valid user.
    return crud.create_task(db , task , user_id)

# STEP 3: Remove user_id from update/delete if possible
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
@limiter.limit("10/minute")
def update_task_status(
    request : Request ,
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
@limiter.limit("10/minute")
def delete_task_by_id(request : Request ,task_id:int , db: db_dep, current_user: user_dep):
    user_id = current_user["user_id"]
    task = crud.delete_task(db , task_id, user_id)
    if not task : 
        raise HTTPException(status_code=404 , detail="Task not found")
    return {"message":"Task deleted successfully"}

# --- AUTHENTICATION ---
@app.post("/login", response_model=schemas.Token, tags=["Authentication"])
@limiter.limit("5/minute")
def login(request : Request ,email:str , password : str ,db : db_dep):
    user = crud.get_user_by_email(db, email)
    if not user or not verify_pass(password, user.password): 
        raise HTTPException(status_code=401 , detail="Invalid email or password")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
@app.post("/chat",response_model=schemas.ChatResponse, tags=["Chat"])
@limiter.limit("20/minute")
def chat(request : Request , body : schemas.ChatRequest , db : db_dep , current_user : user_dep):
    user_id = current_user["user_id"]

    conversation = crud.get_or_create_conversation(db , user_id , body.conversation_id)
    history = crud.get_conversation_messages(db,conversation.id)
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for msg in history :
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": body.message})
    crud.save_message(db,conversation.id,"user",body.message)
    response = groq_client.chat.completions.create(model="llama-3.3-70b-versatile",
        messages=messages,)
    reply = response.choices[0].message.content
    crud.save_message(db,conversation.id,"assistant",reply)
    return {"conversation_id":conversation.id,"reply":reply}