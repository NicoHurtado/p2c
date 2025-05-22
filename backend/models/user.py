from beanie import Document
from pydantic import EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Literal
from uuid import uuid4


class User(Document):
    id: str = str(uuid4())
    username: str
    email: EmailStr
    password_hash: str
    created_at: datetime = datetime.utcnow()
    plan: Literal["free", "pro"] = "free"
    plan_expiration: Optional[datetime] = None
    preferences: Optional[List[str]] = None  # Temas de interés
    learning_style: Optional[str] = None  # Estilo de aprendizaje (visual, auditivo, etc.)
    personality: Optional[List[str]] = None  # Rasgos de personalidad
    profile_type: Optional[str] = None  # Tipo de perfil (estudiante, autodidacta, etc.)
    completed_setup: Optional[bool] = False  # Si ha completado la encuesta inicial
    payment_references: Optional[List[Dict]] = None  # Referencias de pago para seguimiento
    course_limit: int = 1  # Para usuarios free, se actualiza a -1 para pro

    class Settings:
        name = 'users'
