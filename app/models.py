from sqlalchemy import Integer , String , Boolean , Column , ForeignKey, BigInteger , DateTime
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime

class User(Base):
    """
    Represents a system user.
    """
    __tablename__ = "user"
    id = Column(Integer , primary_key=True , nullable=False)
    email = Column(String , unique=True , nullable=True)
    contact_num = Column(String,unique=True , nullable=False)
    task = relationship("Task",back_populates="user")
    password =  Column(String,nullable=False)
    conversation = relationship("Conversation",back_populates="user")

class Task(Base):
    """
    Represents a task assigned to a specific user.
    """
    __tablename__ = "task"
    id = Column(Integer, nullable=False , primary_key=True)
    title = Column(String , nullable=False)
    completed = Column(Boolean , default=False)
    user_id = Column(Integer , ForeignKey("user.id") , nullable=False)
    user = relationship("User",back_populates="task")
    created_at = Column(DateTime , default=datetime.utcnow)
    priority =   Column(String , default="medium", nullable=True)

class Conversation(Base):
    __tablename__ = "conversation"
    id = Column(Integer , primary_key=True , nullable=False)
    user_id = Column(Integer , ForeignKey("user.id") , nullable=False)
    created_at = Column(DateTime , default=datetime.utcnow)
    user = relationship("User",back_populates="conversation")
    messages = relationship("Message",back_populates="conversation")

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer , primary_key=True , nullable=False)
    conversation_id = Column(Integer , ForeignKey("conversation.id") , nullable=False)
    role = Column(String , nullable=False)
    content = Column(String , nullable=False)
    created_at = Column(DateTime , default=datetime.utcnow)
    conversation = relationship("Conversation",back_populates="messages")