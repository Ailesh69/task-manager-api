from sqlalchemy import Integer , String , Boolean , Column , ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer , primary_key=True , nullable=False)
    email = Column(String , unique=True , nullable=True)
    contact_num = Column(String,unique=True , nullable=False)
    task = relationship("Task",back_populates="user")

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, nullable=False , primary_key=True)
    title = Column(String , nullable=False)
    completed = Column(Boolean , default=False)
    user_id = Column(Integer , ForeignKey("user.id") , nullable=False)
    user = relationship("User",back_populates="task")