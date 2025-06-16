import requests
import json

def compare_responses():
    print("🔍 Comparing short vs long prompt responses...")
    print("=" * 60)
    
    # Test prompt corto
    short_data = {'prompt': 'IA', 'level': 'principiante', 'interests': ['tecnología']}
    print("📤 Testing short prompt:", short_data)
    short_response = requests.post('http://localhost:8000/api/courses/generate', json=short_data)
    
    # Test prompt largo  
    long_data = {'prompt': 'Quiero aprender inteligencia artificial desde cero para aplicarla en mis proyectos personales', 'level': 'principiante', 'interests': ['tecnología']}
    print("📤 Testing long prompt:", long_data['prompt'][:50] + "...")
    long_response = requests.post('http://localhost:8000/api/courses/generate', json=long_data)
    
    print('\n=== PROMPT CORTO (IA) ===')
    print('Status:', short_response.status_code)
    if short_response.status_code == 200:
        short_json = short_response.json()
        print('Keys:', list(short_json.keys()))
        print('Course ID:', short_json.get('course_id'))
        print('Has metadata:', 'metadata' in short_json)
        print('Status field:', short_json.get('status'))
        print('Introduction ready:', short_json.get('introduction_ready'))
        
        if 'metadata' in short_json:
            metadata = short_json['metadata']
            print('Metadata keys:', list(metadata.keys()))
            print('Title:', metadata.get('title', 'N/A')[:100])
            print('Description length:', len(metadata.get('description', '')))
            print('Level:', metadata.get('level'))
            print('Total modules:', metadata.get('total_modules'))
            print('Module list length:', len(metadata.get('module_list', [])))
            
            # Check for any empty or invalid fields
            for key, value in metadata.items():
                if not value or (isinstance(value, list) and len(value) == 0):
                    print(f'⚠️  Empty field in metadata: {key} = {value}')
    else:
        print('Error:', short_response.text)

    print('\n=== PROMPT LARGO ===')
    print('Status:', long_response.status_code)
    if long_response.status_code == 200:
        long_json = long_response.json()
        print('Keys:', list(long_json.keys()))
        print('Course ID:', long_json.get('course_id'))
        print('Has metadata:', 'metadata' in long_json)
        print('Status field:', long_json.get('status'))
        print('Introduction ready:', long_json.get('introduction_ready'))
        
        if 'metadata' in long_json:
            metadata = long_json['metadata']
            print('Metadata keys:', list(metadata.keys()))
            print('Title:', metadata.get('title', 'N/A')[:100])
            print('Description length:', len(metadata.get('description', '')))
            print('Level:', metadata.get('level'))
            print('Total modules:', metadata.get('total_modules'))
            print('Module list length:', len(metadata.get('module_list', [])))
            
            # Check for any empty or invalid fields
            for key, value in metadata.items():
                if not value or (isinstance(value, list) and len(value) == 0):
                    print(f'⚠️  Empty field in metadata: {key} = {value}')
    else:
        print('Error:', long_response.text)
    
    print('\n🔍 COMPARISON SUMMARY:')
    if short_response.status_code == 200 and long_response.status_code == 200:
        short_json = short_response.json()
        long_json = long_response.json()
        
        # Compare structure
        short_keys = set(short_json.keys())
        long_keys = set(long_json.keys())
        print(f"Keys match: {short_keys == long_keys}")
        
        if 'metadata' in short_json and 'metadata' in long_json:
            short_meta_keys = set(short_json['metadata'].keys())
            long_meta_keys = set(long_json['metadata'].keys())
            print(f"Metadata keys match: {short_meta_keys == long_meta_keys}")
            
            # Check if short response has all required fields
            required_fields = ['title', 'description', 'level', 'total_modules', 'module_list']
            missing_fields = []
            for field in required_fields:
                if field not in short_json['metadata'] or not short_json['metadata'][field]:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"⚠️  Short response missing/empty fields: {missing_fields}")
            else:
                print("✅ Short response has all required fields")

if __name__ == "__main__":
    compare_responses() 