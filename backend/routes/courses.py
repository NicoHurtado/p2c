from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any, Optional
import uuid
import secrets
from datetime import datetime, timedelta

from models.user import User
from utils.auth import get_current_user
from controllers.course_controller import CourseController
from services.openai_service import generate_text_to_speech

# Pydantic models for requests and responses
from pydantic import BaseModel, EmailStr

class Module(BaseModel):
    title: str
    steps: List[str]
    example: Optional[str] = ""

class CourseRequest(BaseModel):
    topic: str
    experience_level: str
    available_time: str
    demo: Optional[bool] = False

class CourseResponse(BaseModel):
    title: str
    objective: str
    prerequisites: List[str]
    definitions: List[str]
    roadmap: Dict[str, List[str]]
    modules: List[Module]
    resources: List[str]
    faqs: List[str]
    errors: List[str]
    downloads: List[str]
    summary: str
    is_demo: Optional[bool] = False
    demo_message: Optional[str] = None

class SavedCourseRequest(BaseModel):
    title: str
    prompt: str
    content: Dict[str, Any]
    experience_level: str
    available_time: str

class TopicReplacementRequest(BaseModel):
    course_id: str
    section: str
    current_topic: str
    experience_level: str

class ModuleReplacementRequest(BaseModel):
    course_id: str
    module_index: int
    current_module_title: str
    experience_level: str

class CompleteModuleRequest(BaseModel):
    module_id: str

class ShareCourseRequest(BaseModel):
    course_id: str
    email: EmailStr
    message: Optional[str] = None

class CourseQuestion(BaseModel):
    question: str

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "alloy"  # Valores posibles: alloy, echo, fable, onyx, nova, shimmer

# Almacenamiento temporal para tokens de compartir (en producción, usar base de datos)
share_tokens = {}

# Create router
router = APIRouter()

@router.post("/generate-course", response_model=CourseResponse)
async def generate_course(request: CourseRequest, current_user: User = Depends(get_current_user)):
    """Generate a course with AI"""
    return await CourseController.generate_course(
        topic=request.topic,
        experience_level=request.experience_level,
        available_time=request.available_time,
        current_user=current_user
    )

@router.post("/generate-demo", response_model=CourseResponse)
async def generate_demo_course(request: CourseRequest):
    """Generate a demo course without authentication"""
    return await CourseController.generate_course(
        topic=request.topic,
        experience_level=request.experience_level,
        available_time=request.available_time,
        is_demo=True
    )

@router.post("/save-course")
async def save_course(course_data: SavedCourseRequest, current_user: User = Depends(get_current_user)):
    """Save a generated course"""
    return await CourseController.save_course(
        title=course_data.title,
        prompt=course_data.prompt,
        content=course_data.content,
        experience_level=course_data.experience_level,
        available_time=course_data.available_time,
        current_user=current_user
    )

@router.get("/courses")
async def get_courses(current_user: User = Depends(get_current_user)):
    """Get all courses for the current user"""
    return await CourseController.get_user_courses(current_user)

@router.get("/courses/{course_id}")
async def get_course(course_id: str, current_user: User = Depends(get_current_user)):
    """Get a specific course by ID"""
    return await CourseController.get_course_by_id(course_id, current_user)

@router.delete("/courses/{course_id}")
async def delete_course(course_id: str, current_user: User = Depends(get_current_user)):
    """Delete a course"""
    return await CourseController.delete_course(course_id, current_user)

@router.post("/replace-topic")
async def replace_topic(request: TopicReplacementRequest, current_user: User = Depends(get_current_user)):
    """Replace a specific topic in a course with AI-generated content"""
    return await CourseController.replace_topic(
        course_id=request.course_id,
        section=request.section,
        current_topic=request.current_topic,
        experience_level=request.experience_level,
        current_user=current_user
    )

@router.post("/replace-module")
async def replace_module(request: ModuleReplacementRequest, current_user: User = Depends(get_current_user)):
    """Replace a specific module in a course with AI-generated content"""
    return await CourseController.replace_module(
        course_id=request.course_id,
        module_index=request.module_index,
        current_module_title=request.current_module_title,
        experience_level=request.experience_level,
        current_user=current_user
    )

@router.patch("/courses/{course_id}/complete-module")
async def complete_module(
    course_id: str, 
    request: CompleteModuleRequest, 
    current_user: User = Depends(get_current_user)
):
    """Mark a module as completed"""
    return await CourseController.complete_module(
        course_id=course_id,
        module_id=request.module_id,
        current_user=current_user
    )

@router.post("/courses/{course_id}/ask")
async def ask_question(
    course_id: str,
    question: CourseQuestion,
    current_user: User = Depends(get_current_user)
):
    """Ask a question about a course"""
    # Primero obtenemos el curso
    course = await CourseController.get_course_by_id(course_id, current_user)
    
    # Implementar lógica para responder preguntas sobre el curso
    # Esto podría ser un llamado a OpenAI con el contexto del curso
    # Por ahora devolvemos una respuesta de ejemplo
    
    return {
        "question": question.question,
        "answer": f"Esta es una respuesta de ejemplo para tu pregunta sobre {course['title']}. En la implementación real, utilizaríamos OpenAI para generar una respuesta basada en el contenido del curso."
    }

@router.post("/courses/share")
async def share_course(
    request: ShareCourseRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Share a course with someone via email"""
    # Verificar que el curso existe y pertenece al usuario
    course = await CourseController.get_course_by_id(request.course_id, current_user)
    
    # Generar token único para compartir (válido por 7 días)
    token = secrets.token_urlsafe(16)
    expiration = datetime.utcnow() + timedelta(days=7)
    
    # Guardar token con información del curso
    share_tokens[token] = {
        "course_id": request.course_id,
        "expiration": expiration,
        "shared_by": current_user.id
    }
    
    # En producción, enviar email real
    # Aquí simulamos el envío de email como tarea en segundo plano
    # background_tasks.add_task(send_share_email, request.email, token, request.message)
    
    shared_url = f"/courses/shared/{token}"
    
    return {
        "success": True,
        "message": f"Enlace de curso compartido con {request.email}",
        "shared_url": shared_url,
        "expiration": expiration.isoformat()
    }

@router.get("/courses/shared/{token}")
async def view_shared_course(token: str):
    """View a shared course using a token"""
    # Verificar que el token existe y no ha expirado
    if token not in share_tokens:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enlace de curso compartido no válido o expirado"
        )
    
    share_info = share_tokens[token]
    
    # Verificar expiración
    if datetime.utcnow() > share_info["expiration"]:
        # Limpieza de token expirado
        del share_tokens[token]
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="El enlace de curso compartido ha expirado"
        )
    
    # En una implementación real, obtendríamos el curso directamente de la base de datos
    # Sin requerir autenticación para este endpoint específico
    # Por ahora, devolvemos información simulada
    
    return {
        "is_shared": True,
        "course_id": share_info["course_id"],
        "shared_by": share_info["shared_by"],
        "message": "Este es un curso compartido. Para guardar este curso en tu cuenta, debes iniciar sesión o registrarte."
    }

@router.post("/tts/generate")
async def generate_tts(request: TTSRequest, current_user: User = Depends(get_current_user)):
    """Generate text-to-speech audio from text"""
    # Validar el texto
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El texto debe contener al menos 10 caracteres"
        )
    
    # Validar la voz seleccionada
    valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    if request.voice not in valid_voices:
        request.voice = "alloy"  # Voz por defecto
    
    # Generar audio
    audio_data = await generate_text_to_speech(request.text, request.voice)
    
    if not audio_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al generar el audio. Intente nuevamente."
        )
    
    return {
        "success": True,
        "audio_data": audio_data,
        "text_length": len(request.text),
        "voice": request.voice
    } 