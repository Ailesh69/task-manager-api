from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseUser(BaseModel): 
    email : str 
    contact_num : str
class CreateUser(BaseUser):
    pass 

class UserResponse(BaseUser):
    id : int 
    model_config = ConfigDict(from_attributes=True)

class BaseTask(BaseModel):
    title : str 
    completed : Optional[bool] = False 

class CreateTask(BaseTask):
    pass 

class TaskResponse(BaseTask):
    id : int 
    user_id : int 
    model_config = ConfigDict(from_attributes=True)
