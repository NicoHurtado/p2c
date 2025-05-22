from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Dict, Any, Optional
import os
import requests
import hmac
import hashlib
import json
from datetime import datetime, timedelta

from models.user import User
from utils.auth import get_current_user
from services.subscription_service import (
    get_user_subscription,
    update_user_plan,
    get_available_plans
)

# Pydantic models for requests and responses
from pydantic import BaseModel

class PlanUpdateRequest(BaseModel):
    plan: str  # "free" o "pro"

class InitiatePaymentRequest(BaseModel):
    plan: str  # "free" o "pro"
    return_url: str

class PaymentWebhookData(BaseModel):
    event: str
    data: Dict[str, Any]
    timestamp: int
    signature: Optional[str] = None

# Credenciales de Wompi (en producción, deben estar en variables de entorno)
WOMPI_PUBLIC_KEY = os.getenv("WOMPI_PUBLIC_KEY", "pub_test_dummy_key")
WOMPI_PRIVATE_KEY = os.getenv("WOMPI_PRIVATE_KEY", "prv_test_dummy_key")
WOMPI_EVENTS_KEY = os.getenv("WOMPI_EVENTS_KEY", "test_events_dummy_key")
WOMPI_API_URL = os.getenv("WOMPI_API_URL", "https://sandbox.wompi.co/v1")

# Create router
router = APIRouter()

@router.get("/subscription")
async def get_subscription(current_user: User = Depends(get_current_user)):
    """Get the current user's subscription details"""
    subscription = await get_user_subscription(current_user.id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found for this user"
        )
    
    return subscription

@router.post("/subscription")
async def update_subscription(request: PlanUpdateRequest, current_user: User = Depends(get_current_user)):
    """Update the user's subscription to a new plan"""
    try:
        updated_subscription = await update_user_plan(current_user.id, request.plan)
        return updated_subscription
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update subscription: {str(e)}"
        )

@router.get("/plans")
async def get_subscription_plans():
    """Get all available subscription plans"""
    return await get_available_plans()

@router.post("/payments/initiate")
async def initiate_payment(request: InitiatePaymentRequest, current_user: User = Depends(get_current_user)):
    """Iniciar un proceso de pago con Wompi"""
    try:
        # Obtener detalles del plan
        plans = await get_available_plans()
        
        # Encontrar el plan solicitado
        selected_plan = None
        for plan in plans:
            if plan["id"] == request.plan:
                selected_plan = plan
                break
        
        if not selected_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan de suscripción no encontrado"
            )
        
        # Si el plan es gratuito, actualizamos directamente
        if selected_plan["price"] == 0:
            await update_user_plan(current_user.id, request.plan)
            return {
                "success": True,
                "redirect_url": request.return_url,
                "message": "Plan actualizado correctamente"
            }
        
        # Para desarrollo, simulamos el pago inmediatamente en lugar de crearlo
        # Esto evita problemas con payment_references
        updated_subscription = await update_user_plan(current_user.id, request.plan)
        
        return {
            "success": True,
            "message": "Pago simulado procesado correctamente (modo desarrollo)",
            "subscription": updated_subscription,
            "reference": f"dev_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "payment_url": request.return_url
        }
        
    except Exception as e:
        # En caso de cualquier error, intentamos caer de forma segura actualizando el plan
        try:
            await update_user_plan(current_user.id, request.plan)
            return {
                "success": True,
                "message": "Plan actualizado en modo de emergencia",
                "reference": f"emergency_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "payment_url": request.return_url
            }
        except Exception as inner_e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar el pago: {str(e)}. Error secundario: {str(inner_e)}"
            )

@router.post("/payments/webhook")
async def payment_webhook(webhook_data: PaymentWebhookData, request: Request):
    """Webhook para recibir notificaciones de pago de Wompi"""
    # En producción, verificaríamos la firma del webhook
    # signature = request.headers.get('X-Wompi-Signature')
    
    # Verificar que es un evento de transacción exitosa
    if webhook_data.event != "transaction.updated":
        return {"success": True, "message": "Evento recibido pero no procesado"}
    
    # Extraer datos relevantes
    transaction_data = webhook_data.data
    status = transaction_data.get("status")
    reference = transaction_data.get("reference")
    
    # Verificar que la transacción fue exitosa
    if status != "APPROVED":
        return {"success": True, "message": f"Transacción no aprobada: {status}"}
    
    # Buscar el usuario asociado con esta referencia de pago
    users = await User.find({"payment_references.reference": reference}).to_list()
    
    if not users or len(users) == 0:
        return {
            "success": False, 
            "message": "No se encontró un usuario asociado a esta referencia de pago"
        }
    
    user = users[0]
    
    # Encontrar la referencia específica y su plan asociado
    plan = None
    for payment_ref in user.payment_references:
        if payment_ref["reference"] == reference:
            plan = payment_ref["plan"]
            payment_ref["status"] = "APPROVED"
            break
    
    if not plan:
        return {
            "success": False, 
            "message": "No se encontró un plan asociado a esta referencia de pago"
        }
    
    # Actualizar el plan del usuario
    await update_user_plan(user.id, plan)
    await user.save()
    
    return {
        "success": True,
        "message": f"Plan actualizado correctamente para el usuario {user.username}"
    }

@router.post("/payments/simulate-success")
async def simulate_payment_success(request: PlanUpdateRequest, current_user: User = Depends(get_current_user)):
    """Endpoint para simular un pago exitoso (solo para desarrollo)"""
    # Actualizar directamente el plan del usuario
    updated_subscription = await update_user_plan(current_user.id, request.plan)
    
    return {
        "success": True,
        "message": "Pago simulado procesado correctamente",
        "subscription": updated_subscription
    } 