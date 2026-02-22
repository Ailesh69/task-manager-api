from sqlalchemy.orm import Session 
from . import schemas , models 
from .auth import hash_pass
from typing import List, Optional

def create_user(db : Session , user : schemas.CreateUser) -> models.User:
    """Creates a new user with a hashed password."""
    hashed_pass = hash_pass(user.password)
    db_user = models.User(email = user.email , contact_num = user.contact_num , password = hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db:Session ) -> List[models.User]:
    """Retrieves all users."""
    return db.query(models.User).all()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Finds a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_contact(db: Session, contact_num: str) -> Optional[models.User]:
    """Finds a user by their contact number."""
    return db.query(models.User).filter(models.User.contact_num == contact_num).first()

def get_user_by_id(db:Session , id:int) -> Optional[models.User]:
    """Finds a user by their primary key ID."""
    return db.query(models.User).filter(models.User.id == id).first()

def create_task(db:Session , task:schemas.CreateTask , user_id : int) -> models.Task:
    """Creates a task for a specific user."""
    db_task = models.Task(title = task.title , completed = task.completed , user_id = user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task 

def get_task_by_user(db:Session ,user_id : int ) -> List[models.Task]:
        """Retrieves all tasks belonging to a specific user."""
        return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def update_task(db:Session , task_id : int , completed : bool, user_id: int):
    """Updates the completion status of a task, ensuring it belongs to the specified user."""
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if task : 
          task.completed = completed
          db.commit()
          db.refresh(task)
    return task 

def delete_task(db:Session , task_id : int, user_id: int) -> Optional[models.Task]:
    """Deletes a task from the database, ensuring it belongs to the specified user."""
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user_id).first()
    if task : 
         db.delete(task)
         db.commit()
    return task
