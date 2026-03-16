from pydantic import BaseModel, ConfigDict , field_validator , EmailStr
from typing import Optional
import re

# --- USER SCHEMAS ---
class BaseUser(BaseModel): 
    email : EmailStr
    contact_num : str

    @field_validator("contact_num")
    @classmethod
    def valid_contact(cls,v):
        if not re.fullmatch(r"\d{10}",v):
            raise ValueError("Invalid contact number it must be exactly 10 digits")
        return v

class CreateUser(BaseUser):
    password : str

    @field_validator("password")
    @classmethod
    def valid_pass(cls,v):
        if len(v) < 8 :
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"\d",v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserResponse(BaseUser):
    id : int 
    model_config = ConfigDict(from_attributes=True)

# --- TASK SCHEMAS ---
class BaseTask(BaseModel):
    title : str 
    completed : Optional[bool] = False

    @field_validator("title")
    @classmethod
    def valid_title(cls,v):
        if not v.strip():
            raise ValueError("Task title cannot be blank")
        if len(v) > 100 :
            raise ValueError("Task title cannot be longer than 100 characters")
        return v.strip()

class CreateTask(BaseTask):
    priority : Optional[str] = "medium"

    @field_validator("priority")
    @classmethod
    def valid_priority(cls,v):
        if v not in ["low","medium","high"]:
            raise ValueError("Priority must be one of low,medium,high")
        return v

class TaskResponse(BaseTask):
    id : int 
    user_id : int 
    model_config = ConfigDict(from_attributes=True)

# --- AUTH SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str

#---- CHAT SCHEMAS ---
class ChatRequest(BaseModel):
    message : str
    conversation_id: Optional[int] = None
    @field_validator("message")
    @classmethod
    def valid_message(cls,v):
        if not v.strip():
            raise ValueError("Message cannot be blank")
        if len(v) > 1000 :
            raise ValueError("Message cannot be longer than 1000 characters")
        return v.strip()

class MessageResponse(BaseModel):
    id : str
    role : str
    content : str
    created_at : str

    model_config = ConfigDict(from_attributes=True)
class ChatResponse(BaseModel):
    conversation_id: int
    reply : str

