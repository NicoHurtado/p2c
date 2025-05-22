from beanie import Document
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


class Course(Document):
    id: str = str(uuid4())
    user_id: str  # referenciando ID del usuario
    title: str
    prompt: str
    content: Dict  # JSON-like content
    experience_level: str
    available_time: str
    created_at: datetime = datetime.utcnow()
    progress: Optional[Dict] = None  # Para guardar los módulos completados
    tags: Optional[List[str]] = None  # Para clasificar el curso

    class Settings:
        name = 'courses'
