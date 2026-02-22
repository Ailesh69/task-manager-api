from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- USER SCHEMAS ---
class BaseUser(BaseModel): 
    email : str 
    contact_num : str

class CreateUser(BaseUser):
    password : str

class UserResponse(BaseUser):
    id : int 
    model_config = ConfigDict(from_attributes=True)

# --- TASK SCHEMAS ---
class BaseTask(BaseModel):
    title : str 
    completed : Optional[bool] = False 

class CreateTask(BaseTask):
    pass 

class TaskResponse(BaseTask):
    id : int 
    user_id : int 
    model_config = ConfigDict(from_attributes=True)

# --- AUTH SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str
