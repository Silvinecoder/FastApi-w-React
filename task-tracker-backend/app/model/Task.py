import uuid

from sqlalchemy import Column, UUID, String, Boolean, ForeignKey, DateTime, func
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.assistant.model_helper import Base

from app.model.User import User

class TaskTable(Base):
    __tablename__ = 'task'
    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        nullable=False
    )
    title = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    is_complete = Column(Boolean)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('user.uuid'))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    @classmethod
    def get_or_create(cls, session, title, description, is_complete, user_uuid, created_at, updated_at):
        task = session.query(cls).filter_by(title=title, user_uuid=user_uuid).first()
        if task is None:
            task = TaskTable(
                title=title,
                description=description,
                is_complete=is_complete,
                user_uuid=user_uuid,
                created_at=created_at,
                updated_at=updated_at
            )
            session.add(task)
        return task

    class Config:
        orm_mode = True

class Task(BaseModel):
    uuid: uuid.UUID
    title: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=100)
    is_complete : bool
    user_uuid : uuid.UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)