from sqlalchemy.orm import sessionmaker , declarative_base 
from sqlalchemy import create_engine 
from .config import DATABASE_URL

# Create the SQLAlchemy engine using the URL from config
engine = create_engine(DATABASE_URL)

# SessionLocal class for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base() 

def open_db():
    """Dependency to provide a database session to routes."""
    db = SessionLocal() 
    try : 
        yield db 
    finally:
        db.close()
