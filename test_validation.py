#!/usr/bin/env python3
"""
Test script to debug validation issues
"""

import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

from app.models.course import CourseGenerationRequest, CourseLevel

def test_validation():
    print("🧪 Testing CourseGenerationRequest validation...")
    
    # Test data similar to what frontend sends
    test_cases = [
        {
            'name': 'Valid with interests',
            'data': {
                'prompt': 'Quiero aprender IA',
                'level': 'principiante', 
                'interests': ['tecnología']
            }
        },
        {
            'name': 'Valid without interests',
            'data': {
                'prompt': 'Quiero aprender Python',
                'level': 'intermedio', 
                'interests': []
            }
        },
        {
            'name': 'Empty prompt (should fail)',
            'data': {
                'prompt': '',
                'level': 'principiante', 
                'interests': ['programación']
            }
        },
        {
            'name': 'Invalid level (should fail)',
            'data': {
                'prompt': 'Test prompt',
                'level': 'invalid_level', 
                'interests': ['test']
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"   Data: {test_case['data']}")
        
        try:
            request = CourseGenerationRequest(**test_case['data'])
            print(f"   ✅ Validation passed!")
            print(f"   📄 Request object: {request.dict()}")
        except Exception as e:
            print(f"   ❌ Validation failed: {str(e)}")
            print(f"   🔍 Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_validation() 