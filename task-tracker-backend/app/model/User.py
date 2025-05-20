import uuid
from sqlalchemy import Column, UUID, String, DateTime, func
from pydantic import BaseModel, Field, field_validator

from app.assistant.model_helper import Base

class UserTable(Base):
    __tablename__ = 'user'
    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        nullable=False
    )
    email = Column(String(30), nullable=False)
    password_hash = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    @classmethod
    def get_or_create(cls, session, email, password_hash, created_at, updated_at):
        user = session.query(cls).filter_by(email=email).first()
        if user is None:
            user = cls(
                email=email,
                password_hash=password_hash,
                created_at=created_at,
                updated_at=updated_at
            )
            session.add(user)
        return user

class User(BaseModel):
    uuid: uuid.UUID
    email: str = Field(max_length=30)
    password_hash: str = Field(max_length=10)

@field_validator('password_hash')
def check_passwords_match(cls, value):
    if len(value) > 10:
        raise ValueError('Password is too long')
    if not any (c.isupper() for c in value):
        raise ValueError('Password must have a capital letter')
    if not any (c.isdigit() for c in value):
        raise ValueError('Password must have a number')
    if not any (c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in value):
        raise ValueError('Password must have a symbol')
    return value