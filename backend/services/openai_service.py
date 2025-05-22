import os
import json
import re
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import openai
import base64

load_dotenv()

# API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def build_prompt(user_profile: Optional[Dict] = None, topic: str = "", experience_level: str = "", available_time: str = "", pdf_context: Optional[str] = None) -> str:
    """
    Construye un prompt enriquecido con los datos del usuario
    """
    # Prompt base
    base_prompt = f"""Create a structured course about {topic} for a {experience_level} learner with {available_time} of study time available."""
    
    # Añadir contexto de perfil del usuario si está disponible
    if user_profile:
        preferences = user_profile.get("preferences", [])
        learning_style = user_profile.get("learning_style", "")
        personality = user_profile.get("personality", [])
        profile_type = user_profile.get("profile_type", "")
        
        profile_context = ""
        
        if preferences:
            profile_context += f"\nThe learner is interested in: {', '.join(preferences)}."
        
        if learning_style:
            profile_context += f"\nThe learner has a {learning_style} learning style."
        
        if personality:
            profile_context += f"\nThe learner's personality traits include: {', '.join(personality)}."
        
        if profile_type:
            profile_context += f"\nThe learner identifies as a {profile_type}."
        
        if profile_context:
            base_prompt += "\n\nLearner profile:" + profile_context
    
    # Añadir contexto del PDF si está disponible
    if pdf_context:
        base_prompt += f"\n\nPlease incorporate the following reference material in the course when relevant:\n{pdf_context}"
    
    # Instrucciones para el formato de salida
    output_format = """
Your output should be a structured JSON with the following format:
{
  "title": "Course title",
  "objective": "A concise paragraph explaining what the student will learn",
  "prerequisites": ["prerequisite 1", "prerequisite 2", ...],
  "definitions": ["concept 1: explanation", "concept 2: explanation", ...],
  "roadmap": {"Week 1": ["topic 1", "topic 2"], "Week 2": ["topic 3", "topic 4"], ...},
  "modules": [
    {
      "title": "Module title",
      "steps": ["step 1", "step 2", ...],
      "example": "An example related to the module (optional)"
    },
    ...
  ],
  "resources": ["resource 1", "resource 2", ...],
  "faqs": ["Q: question? A: answer", ...],
  "errors": ["Common error 1: How to fix it", ...],
  "downloads": ["name - URL", ...],
  "summary": "A concise summary of the entire course content"
}

Only respond with the valid JSON, with no explanation or additional text.
Do not include any markdown formatting or code blocks, just the JSON object.
Ensure it's detailed and comprehensive but reasonable for the available time.
Make each module engaging and actionable, with clear steps to follow.
Include practical examples when possible.
"""
    
    # Combinar todo
    full_prompt = base_prompt + output_format
    
    return full_prompt

async def generate_course_with_ai(
    topic: str, 
    experience_level: str, 
    available_time: str, 
    user_profile: Optional[Dict] = None,
    pdf_content: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a complete course structure using OpenAI API
    """
    # Construir el prompt enriquecido
    prompt = build_prompt(
        user_profile=user_profile,
        topic=topic,
        experience_level=experience_level,
        available_time=available_time,
        pdf_context=pdf_content
    )

    try:
        print(f"Sending request to OpenAI API for topic: {topic}")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Can be changed to gpt-4 for better results
            messages=[
                {"role": "system", "content": "You are a course creation assistant that responds only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        print("Received response from OpenAI API")
        ai_response = response.choices[0].message.content
        
        # Log response for debugging
        print(f"Response length: {len(ai_response)}")
        print(f"Response preview: {ai_response[:100]}...")
        
        # Extract JSON object from response
        json_str = extract_json_from_text(ai_response)
        if not json_str:
            print("Failed to extract JSON from response")
            raise ValueError("No valid JSON found in response")
            
        # Parse the JSON string
        course_data = json.loads(json_str)
        
        # Validate basic structure
        required_fields = [
            "title", "objective", "prerequisites", "definitions", 
            "roadmap", "modules", "resources", "faqs", "errors", 
            "downloads", "summary"
        ]
        
        # Add missing fields if needed
        for field in required_fields:
            if field not in course_data:
                if field in ["prerequisites", "definitions", "modules", "resources", "faqs", "errors", "downloads"]:
                    course_data[field] = []
                elif field == "roadmap":
                    course_data[field] = {"Basics": ["Getting Started"]}
                else:
                    course_data[field] = f"Generated {field}"
        
        # Añadir etiquetas basadas en el contenido para facilitar búsquedas
        course_data["tags"] = extract_tags(course_data)
        
        print(f"Successfully generated course: {course_data.get('title', 'Unknown title')}")
        return course_data
        
    except Exception as e:
        print(f"Error generating course: {str(e)}")
        # Return a minimal structure in case of error
        return {
            "title": f"Course on {topic}",
            "objective": f"Learn about {topic} at {experience_level} level in {available_time}",
            "prerequisites": [],
            "definitions": [],
            "roadmap": {"Basics": ["Getting Started", "Core Concepts"]},
            "modules": [
                {
                    "title": f"Introduction to {topic}",
                    "steps": ["Understand the basics", "Practice with examples"],
                    "example": ""
                }
            ],
            "resources": [],
            "faqs": [],
            "errors": [f"Note: There was an error generating detailed content: {str(e)}"],
            "downloads": [],
            "summary": f"A course on {topic} for {experience_level} learners with {available_time} available."
        }

def extract_json_from_text(text: str) -> Optional[str]:
    """
    Extract a JSON object from a text response, handling cases where the JSON might be
    embedded in markdown or surrounded by other text
    """
    # Clean up markdown code blocks
    text = re.sub(r'```json', '', text)
    text = re.sub(r'```', '', text)
    
    # Try to find JSON object boundaries
    json_start = text.find('{')
    json_end = text.rfind('}')
    
    if json_start >= 0 and json_end > json_start:
        # Extract the JSON string
        json_str = text[json_start:json_end+1]
        try:
            # Validate by parsing
            json.loads(json_str)
            return json_str
        except:
            # If parsing fails, log for debugging
            print(f"Failed to parse extracted JSON: {json_str[:100]}...")
    
    # If direct extraction failed, try a more aggressive approach
    try:
        # Look for structured data in any format
        print("Attempting to construct valid JSON from response")
        # Create a fallback JSON with minimal structure
        fallback_json = {
            "title": "Generated Course",
            "objective": "Learn new skills",
            "prerequisites": [],
            "definitions": [],
            "roadmap": {"Basics": ["Getting Started"]},
            "modules": [{"title": "Introduction", "steps": ["Step 1", "Step 2"], "example": ""}],
            "resources": [],
            "faqs": [],
            "errors": [],
            "downloads": [],
            "summary": "Course generated from AI"
        }
        
        # Try to extract meaningful content from the text
        if len(text) > 0:
            lines = text.split('\n')
            for line in lines:
                if "title" in line.lower() and len(line) > 10:
                    fallback_json["title"] = line.split(":", 1)[1].strip() if ":" in line else line.strip()
                    break
            
            fallback_json["summary"] = text[:100] + "..." if len(text) > 100 else text
        
        return json.dumps(fallback_json)
    except Exception as e:
        print(f"Failed to construct fallback JSON: {str(e)}")
        return None

def extract_tags(course_data: Dict[str, Any]) -> List[str]:
    """
    Extrae etiquetas relevantes a partir del contenido del curso
    """
    tags = []
    
    # Añadir título como etiqueta principal
    if "title" in course_data and course_data["title"]:
        title_words = course_data["title"].lower().split()
        for word in title_words:
            if len(word) > 3 and word not in ["with", "from", "that", "this", "and", "for", "the", "course"]:
                tags.append(word)
    
    # Añadir prerrequisitos como posibles etiquetas
    if "prerequisites" in course_data and course_data["prerequisites"]:
        for prereq in course_data["prerequisites"]:
            if ":" in prereq:
                tag = prereq.split(":", 1)[0].strip().lower()
            else:
                tag = prereq.lower().split()[0]
            
            if tag and len(tag) > 3 and tag not in tags:
                tags.append(tag)
    
    # Añadir palabras clave de los módulos
    if "modules" in course_data and course_data["modules"]:
        for module in course_data["modules"]:
            if "title" in module and module["title"]:
                title_words = module["title"].lower().split()
                for word in title_words:
                    if len(word) > 3 and word not in ["introduction", "module", "basic", "advanced"] and word not in tags:
                        tags.append(word)
    
    # Limitar a 10 etiquetas como máximo
    return tags[:10]

async def generate_text_to_speech(text: str, voice: str = "alloy") -> Optional[str]:
    """
    Genera audio a partir de texto usando el API de OpenAI
    """
    try:
        # Verificar que el texto no sea demasiado largo
        if len(text) > 4000:
            text = text[:4000]  # OpenAI TTS tiene un límite de caracteres
            
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # En una implementación real, guardaríamos este archivo y devolveríamos su URL
        # Para este ejemplo, devolvemos una cadena base64 del audio
        audio_data = response.content
        base64_audio = base64.b64encode(audio_data).decode('utf-8')
        
        return f"data:audio/mp3;base64,{base64_audio}"
    except Exception as e:
        print(f"Error generating text-to-speech: {str(e)}")
        return None 