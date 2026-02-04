from fastapi import FastAPI , Depends , HTTPException
from . import models , schemas , crud 
from .db import engine , open_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task manager")

@app.post("/user/", response_model=schemas.UserResponse, tags=["Users"])
def create_user(user : schemas.CreateUser , db : Session = Depends(open_db)):
    return crud.create_user(db , user)

@app.get("/user/", response_model=list[schemas.UserResponse], tags=["Users"])
def get_user(db:Session = Depends(open_db)):
    return crud.get_user(db)

@app.get("/user/{user_id}/task/", response_model=list[schemas.TaskResponse], tags=["Tasks"])
def get_user_task(user_id : int , db:Session = Depends(open_db)):
    return crud.get_task_by_user(db , user_id)

@app.post("/user/{user_id}/task/", response_model=schemas.TaskResponse, tags=["Tasks"])
def create_task_for_user(user_id : int , task : schemas.CreateTask , db:Session = Depends(open_db)):
    user = crud.get_user_by_id(db,user_id)
    if not user : 
        raise HTTPException(status_code=404 , detail="user not found")
    return crud.create_task(db , task , user_id)

@app.put("/user/{user_id}/task/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(user_id: int, task_id:int , completed:bool , db:Session = Depends(open_db)):
    task = crud.update_task(db , task_id , completed)
    if not task : 
        raise HTTPException(status_code=404 , detail="task_not_found")
    return task 

@app.delete("/task/{task_id}", tags=["Tasks"])
def delete_task_by_id(task_id:int , db:Session = Depends(open_db)):
    task = crud.delete_task(db , task_id)
    if not task : 
        raise HTTPException(status_code=404 , detail="task_not_found")
    return {"message":"task deleted successfully"}
