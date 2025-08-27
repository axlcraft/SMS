from sqlalchemy import Column, Float, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base #, relationship
from datetime import datetime

from pydantic import BaseModel, Field
# from typing import Optional

# Define la base declarativa
Base = declarative_base()

# Clase de modelo para las métricas
class Metrics(Base):
    # Nombre de la tabla
    __tablename__ = "metrics"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, autoincrement=True)
    systolic_pressure = Column(Integer, nullable=True)
    diastolic_pressure = Column(Integer, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # user = relationship("User", back_populates="metrics")

    def __repr__(self):
        return f"<YourModel(id={self.id}')>"
    
class MetricsBase(BaseModel):
    systolic_pressure: int = Field(..., ge=50, le=250)   
    diastolic_pressure: int = Field(..., ge=30, le=150) 
    heart_rate: int = Field(None, ge=30, le=220)        
    weight: float = Field(None, gt=0)                   

class MetricsCreate(MetricsBase):
    user_id: int

class MetricsRead(MetricsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
