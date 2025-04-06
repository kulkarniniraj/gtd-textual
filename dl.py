"""
SQLite data layer for GTD app. Use SQLAlchemy ORM to interact with the database.
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, BLOB
from sqlalchemy.orm import sessionmaker, declarative_base

"""
SQLAlchemy model to save each gtd task. 
Columns: id, orderid, title, description, project, create date, update date, done (bool)

"""
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    orderid = Column(Integer)
    title = Column(String)
    description = Column(String)
    project = Column(String)
    tag = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    done = Column(Integer, default=0)  # Using Integer as SQLite doesn't have native boolean

# Generate the table in the database if it doesn't exist
engine = create_engine('sqlite:///gtd.db')
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

def create_empty_task():
    """
    Create a new task with empty fields.
    """
    task = Task(title='', description='', project='default', tag='inbox')
    return task

def save_task(task):
    """
    Save a task to the database.
    """
    if task.created_at is None:
        task.created_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    with Session() as session:
        session.add(task)
        session.commit()


def get_all_tasks():
    """
    Get all tasks from the database.
    """
    with Session() as session:
        tasks = session.query(Task).order_by(Task.orderid).all()
        return tasks
