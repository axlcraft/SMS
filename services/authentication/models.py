from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Base de SQLAlchemy
Base = declarative_base()

# ---------------- TABLAS ----------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)  # guardamos hash, no password
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con sesiones
    sessions = relationship("Session", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session(id={self.id}, session_id='{self.session_id}')>"


# ---------------- SCHEMAS (Pydantic) ----------------

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)  # la password se recibe en texto plano


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SessionRead(BaseModel):
    id: int
    session_id: str
    user_id: int
    expires_at: datetime

    class Config:
        orm_mode = True
