import requests
import json

# Test the health endpoint
try:
    health_response = requests.get("http://localhost:8000/health")
    print("Health check:")
    print(f"Status: {health_response.status_code}")
    print(f"Response: {health_response.json()}")
    print()
except Exception as e:
    print(f"Health check failed: {e}")
    print()

# Test the validation endpoint
try:
    test_data = {
        "prompt": "Quiero aprender inteligencia artificial desde cero para aplicarla en mis proyectos personales",
        "level": "principiante",
        "interests": ["programación", "tecnología", "machine learning", "python"]
    }
    
    validation_response = requests.post(
        "http://localhost:8000/api/courses/test-validation",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Validation test:")
    print(f"Status: {validation_response.status_code}")
    print(f"Response: {validation_response.json()}")
    print()
except Exception as e:
    print(f"Validation test failed: {e}")
    print()

# Test the actual course generation endpoint
try:
    generation_response = requests.post(
        "http://localhost:8000/api/courses/generate",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print("Course generation test:")
    print(f"Status: {generation_response.status_code}")
    if generation_response.status_code == 200:
        print(f"Response: {generation_response.json()}")
    else:
        print(f"Error response: {generation_response.text}")
    print()
except Exception as e:
    print(f"Course generation test failed: {e}")
    print() 