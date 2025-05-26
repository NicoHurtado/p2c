"""
Pydantic schemas for request/response models
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: str
    plan: Optional[str] = "free"
    plan_end_date: Optional[str] = None
    completed_setup: Optional[bool] = False


class ProfileSetupRequest(BaseModel):
    interests: List[str]
    profile_type: str
    personality_traits: List[str]
    learning_style: str


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


# Course generation payload schema
class CourseGenerationRequest(BaseModel):
    prompt: str
    experience_level: str
    personality: str
    learning_style: str


# Subscription schemas
class PlanUpdateRequest(BaseModel):
    plan: str  # "free" or "pro"


class InitiatePaymentRequest(BaseModel):
    plan: str
    return_url: str


class PaymentWebhookData(BaseModel):
    event: str
    data: Dict[str, Any]
    timestamp: int
    signature: Optional[str] = None


# Response schemas
class SuccessResponse(BaseModel):
    success: bool
    message: str


class ErrorResponse(BaseModel):
    detail: str 