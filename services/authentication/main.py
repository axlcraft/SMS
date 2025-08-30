from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, UserCreate, UserLogin, UserRead, Session as DBSession, SessionRead
from database_sql import create_db_and_tables, get_db
from datetime import datetime, timedelta
import secrets
import hashlib
import os


router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "pong"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar la aplicación
    create_db_and_tables()  
    yield
    # Código que se ejecuta al cerrar la aplicación
app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}

# Utilidad para hashear contraseñas
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Endpoint de registro
@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    hashed = hash_password(user.password)
    db_user = User(email=user.email, password_hash=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoint de login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.password_hash != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    # Crear sesión
    session_id = secrets.token_hex(16)
    expires_at = datetime.utcnow() + timedelta(hours=2)
    db_session = DBSession(session_id=session_id, user_id=db_user.id, expires_at=expires_at)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return {"session_id": session_id, "expires_at": expires_at}

# Endpoint para obtener sesiones activas de un usuario
@router.get("/sessions/{user_id}", response_model=list[SessionRead])
def get_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(DBSession).filter(DBSession.user_id == user_id).all()
    return sessions

app.include_router(router, prefix="/auth")

