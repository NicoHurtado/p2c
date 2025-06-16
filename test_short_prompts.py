import requests
import json

# Test prompts cortos que ahora deberían funcionar
short_prompts = [
    "Python",
    "IA",
    "React",
    "ML",
    "CSS",
    "Git",
    "APIs",
    "Diseño",
    "Bases de datos"
]

def test_short_prompts():
    print("🧪 Testing short prompts that should now work...")
    print("=" * 60)
    
    for i, prompt in enumerate(short_prompts, 1):
        print(f"\n{i}. Testing prompt: '{prompt}'")
        
        test_data = {
            "prompt": prompt,
            "level": "principiante",
            "interests": ["programación", "tecnología"]
        }
        
        try:
            json_data = json.dumps(test_data)
            size = len(json_data.encode('utf-8'))
            print(f"   Size: {size} bytes")
            
            response = requests.post(
                "http://localhost:8000/api/courses/generate",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ SUCCESS! Course ID: {data.get('course_id', 'N/A')}")
                print(f"   📚 Title: {data.get('metadata', {}).get('title', 'N/A')[:50]}...")
            else:
                print(f"   ❌ Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   Exception: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_short_prompts() 