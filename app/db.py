from sqlalchemy.orm import sessionmaker , declarative_base 
from sqlalchemy import create_engine 

# Ensure 'ailesh2006' is the correct password and the 'taskmanager' database exists.
engine = create_engine("postgresql://postgres:ailesh2006@localhost:5432/taskmanager")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

def open_db():
    db = SessionLocal() 
    try : 
        yield db 
    finally:
        db.close()
