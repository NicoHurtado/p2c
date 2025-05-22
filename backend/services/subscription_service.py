from typing import Optional, Dict, Any
from models.user import User
from models.course import Course
from fastapi import HTTPException, status
import datetime

async def get_remaining_courses(user: User) -> int:
    """
    Calculate the remaining courses a user can create based on their plan
    """
    # Si el usuario tiene plan pro, tiene cursos ilimitados
    if user.plan == "pro":
        return float('inf')  # Unlimited
    
    # Para usuarios free, verificamos el límite (por defecto es 1)
    limit = user.course_limit
    
    # Contar los cursos existentes del usuario
    existing_courses = await Course.find(Course.user_id == user.id).count()
    
    # Calcular los cursos restantes
    remaining = max(0, limit - existing_courses)
    return remaining

async def get_user_subscription(user_id: str) -> Dict[str, Any]:
    """
    Get a user's current subscription details
    """
    # Buscar el usuario
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verificar si el plan está activo
    is_active = True
    if user.plan == "pro" and user.plan_expiration and user.plan_expiration < datetime.datetime.utcnow():
        is_active = False
    
    # Calcular días restantes si aplica
    remaining_days = None
    if user.plan == "pro" and user.plan_expiration and is_active:
        delta = user.plan_expiration - datetime.datetime.utcnow()
        remaining_days = max(0, delta.days)
    
    # Información de precios y límites
    plan_info = {
        "free": {
            "price": 0,
            "course_limit": 1,
            "description": "Plan gratuito con acceso a 1 curso"
        },
        "pro": {
            "price": 19.90,
            "course_limit": -1,
            "description": "Plan premium con acceso ilimitado a cursos"
        }
    }
    
    plan_data = plan_info[user.plan]
    
    return {
        "plan": user.plan,
        "price": plan_data["price"],
        "course_limit": plan_data["course_limit"],
        "is_active": is_active,
        "expiration": user.plan_expiration.isoformat() if user.plan_expiration else None,
        "remaining_days": remaining_days,
        "description": plan_data["description"]
    }

async def update_user_plan(user_id: str, new_plan: str) -> Dict[str, Any]:
    """
    Update a user's plan to free or pro
    """
    # Validar el usuario
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validar el plan
    if new_plan not in ["free", "pro"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan. Must be 'free' or 'pro'"
        )
    
    # Actualizar el plan
    user.plan = new_plan
    
    # Establecer límites según el plan
    if new_plan == "free":
        user.course_limit = 1
        user.plan_expiration = None
    else:  # pro
        user.course_limit = -1  # ilimitado
        # Establecer fecha de expiración para un mes desde ahora
        user.plan_expiration = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    
    # Guardar cambios
    await user.save()
    
    # Obtener datos actualizados
    return await get_user_subscription(user_id)

async def get_available_plans() -> list:
    """
    Get all available subscription plans
    """
    plans = [
        {
            "id": "free",
            "name": "Free",
            "price": 0,
            "course_limit": 1,
            "description": "Plan gratuito con acceso a 1 curso"
        },
        {
            "id": "pro",
            "name": "Pro",
            "price": 19.90,
            "course_limit": -1,
            "description": "Plan premium con acceso ilimitado a cursos"
        }
    ]
    
    return plans 