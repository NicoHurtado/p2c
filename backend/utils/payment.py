import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from models.user import User
from models.course import Course

# Import the payment service
try:
    from payment_service import create_payment_link, verify_payment, approve_simulated_payment, SIMULATION_MODE
    PAYMENT_ENABLED = True
except ImportError:
    # If the payment service module is not available, disable payment functionality
    PAYMENT_ENABLED = False
    print("WARNING: Payment service not available")

async def is_subscription_active(user: User) -> bool:
    """Check if the user's subscription is still active"""
    if user.plan == "free":
        return True  # Free tier is always active
    
    if not user.plan_expiration:
        return False
    
    return user.plan_expiration > datetime.utcnow()

async def get_remaining_courses(user: User) -> int:
    """Get the number of courses remaining for the user"""
    # Check for pro plan
    if user.plan == "pro":
        return -1  # Unlimited
    
    # For free plan, return course_limit
    return user.course_limit
    
async def create_payment(user: User, plan: str) -> Dict[str, Any]:
    """Create a payment for a subscription"""
    if not PAYMENT_ENABLED:
        return {"success": False, "error": "Payment service is not available"}
    
    # Plan details
    plan_details = {
        "free": {"name": "Free", "price": 0},
        "pro": {"name": "Pro", "price": 19.90}
    }
    
    if plan not in plan_details:
        return {"success": False, "error": "Invalid subscription plan"}
    
    # Create payment
    payment_result = create_payment_link(
        user_id=user.id,
        plan_id=plan,
        plan_name=plan_details[plan]["name"],
        amount=plan_details[plan]["price"]
    )
    
    return payment_result

async def verify_and_update_subscription(user: User, reference: str) -> Dict[str, Any]:
    """Verify a payment and update the user's subscription"""
    if not PAYMENT_ENABLED:
        return {"success": False, "error": "Payment service is not available"}
    
    # Verify payment
    payment_result = verify_payment(reference)
    
    if payment_result["success"] and payment_result["status"] == "APPROVED":
        # Extract plan from reference
        parts = reference.split("_")
        if len(parts) >= 3:
            plan = parts[1]
            
            if plan in ["free", "pro"]:
                # Update user subscription
                user.plan = plan
                user.plan_expiration = datetime.utcnow() + timedelta(days=30) if plan == "pro" else None
                user.course_limit = -1 if plan == "pro" else 1
                await user.save()
                
                return {
                    "success": True,
                    "subscription": {
                        "plan": plan,
                        "expiration": user.plan_expiration.isoformat() if user.plan_expiration else None
                    }
                }
    
    return payment_result

async def approve_simulated_payment_and_update(user: User, reference: str) -> Dict[str, Any]:
    """
    Approve a simulated payment and update the user's subscription
    Only for testing/simulation purposes
    """
    if not PAYMENT_ENABLED or not SIMULATION_MODE:
        return {"success": False, "error": "This function is only available in simulation mode"}
    
    # Approve payment
    payment_result = approve_simulated_payment(reference)
    
    if payment_result["success"]:
        # Extract plan from reference
        parts = reference.split("_")
        if len(parts) >= 3:
            plan = parts[1]
            
            if plan in ["free", "pro"]:
                # Update user subscription
                user.plan = plan
                user.plan_expiration = datetime.utcnow() + timedelta(days=30) if plan == "pro" else None
                user.course_limit = -1 if plan == "pro" else 1
                await user.save()
                
                return {
                    "success": True,
                    "subscription": {
                        "plan": plan,
                        "expiration": user.plan_expiration.isoformat() if user.plan_expiration else None
                    }
                }
    
    return payment_result 