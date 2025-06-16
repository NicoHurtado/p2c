from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
import hashlib


class CourseLevel(str, Enum):
    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"


class CourseStatus(str, Enum):
    GENERATING = "generating"
    READY = "ready"
    ERROR = "error"


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str


class VideoResource(BaseModel):
    youtube_id: str
    title: str
    description: str
    timestamps: List[Dict[str, Union[str, int]]] = []
    embed_url: str
    relevance_score: float = Field(ge=0.0, le=1.0)


class AudioResource(BaseModel):
    original_text: str
    s3_url: Optional[str] = None
    language: str = "es"
    duration: Optional[int] = None  # seconds
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ModuleResources(BaseModel):
    videos: List[VideoResource] = []
    audios: List[AudioResource] = []


class ModuleChunk(BaseModel):
    chunk_id: str
    content: str = Field(max_length=2000)
    total_chunks: int
    chunk_order: int
    checksum: str

    @classmethod
    def create_chunk(cls, content: str, order: int, total: int, module_id: str):
        chunk_id = f"{module_id}_chunk_{order}"
        checksum = hashlib.md5(content.encode()).hexdigest()
        return cls(
            chunk_id=chunk_id,
            content=content,
            total_chunks=total,
            chunk_order=order,
            checksum=checksum
        )


class Module(BaseModel):
    module_id: str
    title: str
    description: str
    objective: str
    concepts: List[str]
    chunks: List[ModuleChunk] = []
    quiz: List[QuizQuestion]
    summary: str
    practical_exercise: str
    resources: ModuleResources = Field(default_factory=ModuleResources)


class CourseMetadata(BaseModel):
    title: str
    description: str = Field(min_length=150, max_length=1000)
    level: CourseLevel
    estimated_duration: int  # hours
    prerequisites: List[str]
    total_modules: int
    module_list: List[str]  # titles of all modules
    topics: List[str]
    total_size: str  # estimated content size


class FinalProject(BaseModel):
    title: str
    description: str
    requirements: List[str]
    deliverables: List[str]
    evaluation_criteria: List[str]


class CertificateTemplate(BaseModel):
    template_id: str
    course_title_placeholder: str = "{{course_title}}"
    student_name_placeholder: str = "{{student_name}}"
    completion_date_placeholder: str = "{{completion_date}}"
    duration_placeholder: str = "{{duration}}"


class Course(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    metadata: CourseMetadata
    modules: List[Module] = []
    user_prompt: str
    user_level: CourseLevel
    user_interests: List[str]
    status: CourseStatus = CourseStatus.GENERATING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    final_project: Optional[FinalProject] = None
    certificate_template: Optional[CertificateTemplate] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "metadata": {
                    "title": "Inteligencia Artificial para Principiantes",
                    "description": "Un curso completo de IA que te llevará desde los conceptos básicos hasta implementaciones prácticas, con ejemplos relacionados a tus intereses en deportes y videojuegos.",
                    "level": "principiante",
                    "estimated_duration": 25,
                    "prerequisites": ["Conocimientos básicos de programación", "Matemáticas de nivel secundario"],
                    "total_modules": 8,
                    "module_list": ["Introducción a la IA", "Machine Learning Básico", "Redes Neuronales"],
                    "topics": ["machine learning", "redes neuronales", "algoritmos", "python"],
                    "total_size": "~500KB de contenido texto"
                },
                "user_prompt": "Quiero aprender inteligencia artificial para mis proyectos",
                "user_level": "principiante",
                "user_interests": ["deportes", "tenis", "videojuegos", "programación"],
                "status": "generating"
            }
        }


# Request/Response models for API
class CourseGenerationRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=500)
    level: CourseLevel
    interests: List[str] = Field(min_items=1, max_items=10)


class CourseGenerationResponse(BaseModel):
    course_id: str
    metadata: CourseMetadata
    status: CourseStatus
    introduction_ready: bool = True


class AudioGenerationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    language: str = "es"


class StreamEvent(BaseModel):
    event_type: str  # "module_ready", "chunk_ready", "course_complete", "error"
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow) 