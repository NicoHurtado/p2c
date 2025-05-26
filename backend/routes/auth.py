from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import uuid

from models.user import User
from utils.auth import (
    create_access_token, 
    authenticate_user, 
    get_password_hash, 
    get_current_user, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from schemas import UserCreate, UserResponse, Token, ProfileSetupRequest

# Create router
router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Check if username exists
    existing_user = await User.find_one(User.username == user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    existing_email = await User.find_one(User.email == user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    # Create and save new user
    new_user = User(
        id=str(uuid.uuid4()),
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        plan="free"
    )
    
    await new_user.insert()
    
    # Create response without password
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        created_at=new_user.created_at.isoformat(),
        plan=new_user.plan,
        plan_end_date=new_user.plan_expiration.isoformat() if new_user.plan_expiration else None,
        completed_setup=new_user.completed_setup
    )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at.isoformat(),
        plan=current_user.plan,
        plan_end_date=current_user.plan_expiration.isoformat() if current_user.plan_expiration else None,
        completed_setup=current_user.completed_setup
    )

@router.post("/profile-setup")
async def setup_user_profile(profile_data: ProfileSetupRequest, current_user: User = Depends(get_current_user)):
    """Setup user profile with preferences after registration"""
    # Actualizar datos del perfil del usuario
    current_user.preferences = profile_data.interests
    current_user.profile_type = profile_data.profile_type
    current_user.personality = profile_data.personality_traits
    current_user.learning_style = profile_data.learning_style
    current_user.completed_setup = True
    
    # Guardar cambios
    await current_user.save()
    
    return {
        "success": True,
        "message": "Perfil de usuario configurado correctamente",
        "profile": {
            "interests": current_user.preferences,
            "profile_type": current_user.profile_type,
            "personality": current_user.personality,
            "learning_style": current_user.learning_style,
            "completed_setup": current_user.completed_setup
        }
    }

@router.get("/stats")
async def get_user_stats(current_user: User = Depends(get_current_user)):
    """Get user statistics and achievements"""
    from models.course import Course
    
    # Contar cursos creados
    courses = await Course.find(Course.user_id == current_user.id).to_list()
    
    # Calcular estadísticas
    total_courses = len(courses)
    completed_modules = 0
    total_modules = 0
    
    for course in courses:
        if hasattr(course, 'content') and 'modules' in course.content:
            total_modules += len(course.content['modules'])
        
        if hasattr(course, 'progress') and course.progress and 'completed_modules' in course.progress:
            completed_modules += len(course.progress['completed_modules'])
    
    # Determinar insignias
    badges = []
    
    if total_courses >= 1:
        badges.append({"id": "first_course", "name": "¡Primera creación!", "description": "Creaste tu primer curso"})
    
    if total_courses >= 5:
        badges.append({"id": "course_master", "name": "Maestro de cursos", "description": "Creaste al menos 5 cursos"})
    
    if completed_modules >= 10:
        badges.append({"id": "quick_learner", "name": "Aprendiz veloz", "description": "Completaste 10 módulos"})
    
    # Calcular nivel del usuario basado en actividad
    level = min(10, 1 + (total_courses // 2) + (completed_modules // 5))
    
    return {
        "stats": {
            "total_courses": total_courses,
            "total_modules": total_modules,
            "completed_modules": completed_modules,
            "completion_rate": (completed_modules / total_modules * 100) if total_modules > 0 else 0
        },
        "badges": badges,
        "level": level,
        "next_badge": {
            "name": "Experto en contenido",
            "description": "Crea 10 cursos para desbloquear esta insignia", 
            "progress": total_courses * 10
        }
    } 