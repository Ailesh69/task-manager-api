from sqlalchemy.orm import Session 
from . import schemas , models 

def create_user(db : Session , user : schemas.CreateUser):
    db_user = models.User(email = user.email , contact_num = user.contact_num)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_user(db:Session ):
    return db.query(models.User).all()
def get_user_by_id(db:Session , id:int):
    return db.query(models.User).filter(models.User.id == id).first()

def create_task(db:Session , task:schemas.CreateTask , user_id : int):
    db_task = models.Task(title = task.title , completed = task.completed , user_id = user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task 

def get_task_by_user(db:Session ,user_id : int ):
        return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def update_task(db:Session , task_id : int , completed : bool):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task : 
          task.completed = completed
          db.commit()
          db.refresh(task)
    return task 
def delete_task(db:Session , task_id : int ):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task : 
         db.delete(task)
         db.commit()
    return task
