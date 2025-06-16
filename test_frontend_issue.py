import requests
import json

# Test different types of invalid requests that might cause 422
test_cases = [
    {
        "name": "Empty request",
        "data": {}
    },
    {
        "name": "Only prompt",
        "data": {"prompt": "test"}
    },
    {
        "name": "Short prompt",
        "data": {
            "prompt": "test",
            "level": "principiante",
            "interests": ["test"]
        }
    },
    {
        "name": "Empty interests",
        "data": {
            "prompt": "Quiero aprender algo interesante",
            "level": "principiante",
            "interests": []
        }
    },
    {
        "name": "Invalid level",
        "data": {
            "prompt": "Quiero aprender algo interesante",
            "level": "beginner",  # Should be "principiante"
            "interests": ["test"]
        }
    },
    {
        "name": "Missing fields",
        "data": {
            "prompt": "Quiero aprender algo interesante"
            # Missing level and interests
        }
    },
    {
        "name": "Null values",
        "data": {
            "prompt": None,
            "level": "principiante",
            "interests": ["test"]
        }
    }
]

def test_invalid_requests():
    print("🧪 Testing different invalid request scenarios...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   Data: {test_case['data']}")
        
        try:
            # Calculate the size of the request
            json_data = json.dumps(test_case['data'])
            size = len(json_data.encode('utf-8'))
            print(f"   Size: {size} bytes")
            
            response = requests.post(
                "http://localhost:8000/api/courses/generate",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Error: {response.text}")
            
            # Check if this matches the 63-byte issue
            if size == 63:
                print("   🎯 THIS MATCHES THE 63-BYTE ISSUE!")
                
        except Exception as e:
            print(f"   Exception: {e}")
        
        print("-" * 40)

def test_debug_endpoint():
    print("\n🔍 Testing debug endpoint...")
    
    # Test with the suspected 63-byte payload
    test_data = {"prompt": "", "level": "principiante", "interests": []}
    
    try:
        response = requests.post(
            "http://localhost:8000/api/courses/debug-request",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Debug response: {response.json()}")
        
    except Exception as e:
        print(f"Debug test failed: {e}")

if __name__ == "__main__":
    test_invalid_requests()
    test_debug_endpoint() 