import json
import re
import logging
from typing import Dict, List
from anthropic import AsyncAnthropic
from ..models.course import CourseMetadata, CourseLevel, Module, ModuleChunk, FinalProject
from ..core.config import get_settings

logger = logging.getLogger(__name__)

class ClaudeService:
    """Service for intelligent content generation using Claude AI"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncAnthropic(api_key=self.settings.anthropic_api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def generate_course_metadata(
        self, 
        user_prompt: str, 
        level: CourseLevel, 
        interests: List[str]
    ) -> CourseMetadata:
        """Generate course metadata using Claude"""
        
        prompt = f"""
        Eres un experto diseñador curricular. Basándote en la solicitud: "{user_prompt}", 
        nivel: "{level}" e intereses: {interests}, genera metadatos para un curso personalizado.
        
        Responde SOLO con JSON válido:
        {{
            "title": "título atractivo del curso",
            "description": "descripción detallada de máximo 800 caracteres que conecte con los intereses",
            "level": "{level}",
            "estimated_duration": 8,
            "prerequisites": ["Requisito 1", "Requisito 2"],
            "total_modules": 5,
            "module_list": ["Módulo 1", "Módulo 2", "Módulo 3", "Módulo 4", "Módulo 5"],
            "topics": ["tema1", "tema2", "tema3", "tema4"],
            "total_size": "estimación de tamaño de contenido"
        }}
        
        IMPORTANTE:
        - La descripción debe tener máximo 800 caracteres (incluyendo espacios)
        - total_modules debe coincidir con la cantidad de elementos en module_list
        - topics debe incluir 4-6 temas principales del curso
        - Conecta cada módulo con los intereses: {', '.join(interests)}
        - Para nivel {level}, ajusta complejidad apropiadamente
        - NO incluyas explicaciones adicionales, SOLO el JSON
        """
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text.strip()
            
            # Clean and parse JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                metadata_dict = json.loads(json_match.group())
                return CourseMetadata(**metadata_dict)
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            logger.error(f"Error generating course metadata: {str(e)}")
            raise
    
    async def generate_course_introduction(
        self, 
        metadata: CourseMetadata, 
        user_prompt: str, 
        interests: List[str]
    ) -> str:
        """Generate course introduction following the specified format"""
        
        prompt = f"""
        Genera la introducción completa para el curso siguiendo EXACTAMENTE este formato:

        📚 **{metadata.title}**
        *(Título atractivo relacionado con {user_prompt} y los intereses {', '.join(interests)})*

        🎉 **Bienvenida**
        ¡Bienvenido/a a este curso personalizado de {user_prompt}!
        A lo largo de este recorrido, exploraremos juntos los principales conceptos y prácticas de {user_prompt}, conectándolos con tus intereses en {', '.join(interests)}.

        **Duración estimada:** {metadata.estimated_duration} horas
        **Nivel seleccionado:** {metadata.level}
        **Enfoque especial:** Ejemplos prácticos relacionados con {', '.join(interests)}

        Prepárate para aprender de forma dinámica y práctica. 🚀

        📝 **Requisitos previos**
        Antes de comenzar, es recomendable que cuentes con:
        {chr(10).join([f'* ✅ {prereq}' for prereq in metadata.prerequisites])}

        📖 **Temas que exploraremos**
        Línea de tiempo interactiva de módulos:

        {chr(10).join([f'📚 Módulo {i+1}: {module} - [Descripción breve personalizada]' for i, module in enumerate(metadata.module_list)])}

        🌟 **¡Empecemos!**
        ¡Vamos allá! 🚀✨

        IMPORTANTE: Personaliza cada descripción breve conectándola con los intereses del usuario.
        """
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Error generating course introduction: {str(e)}")
            raise
    
    async def generate_module_structure(
        self, 
        module_title: str, 
        course_context: str,
        level: CourseLevel,
        interests: List[str],
        module_index: int
    ) -> Dict:
        """Generate module structure without content (for fast initial response)"""
        
        prompt = f"""
        Crea la estructura para el módulo "{module_title}" del curso sobre "{course_context}".
        Nivel: {level}, Intereses del usuario: {', '.join(interests)}
        
        Responde SOLO con JSON:
        {{
            "module_id": "modulo_{module_index + 1}",
            "title": "{module_title}",
            "description": "Descripción del módulo (2-3 líneas)",
            "objective": "Al finalizar este módulo, serás capaz de...",
            "concepts": ["concepto1", "concepto2", "concepto3", "concepto4"],
            "quiz": [
                {{
                    "question": "Pregunta 1",
                    "options": ["opción1", "opción2", "opción3", "opción4"],
                    "correct_answer": 0,
                    "explanation": "Explicación de la respuesta correcta"
                }}
            ],
            "summary": "Resumen de conceptos clave del módulo",
            "practical_exercise": "Ejercicio integrador que combine todos los conceptos"
        }}
        
        IMPORTANTE: Conecta todo con los intereses {', '.join(interests)}
        """
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            logger.error(f"Error generating module structure: {str(e)}")
            raise
    
    async def generate_concept_content(
        self, 
        concept: str, 
        module_context: str,
        course_context: str,
        level: CourseLevel,
        interests: List[str]
    ) -> str:
        """Generate detailed content for a specific concept"""
        
        prompt = f"""
        Genera contenido detallado para el concepto "{concept}" siguiendo este formato:

        📖 **Concepto: {concept}**

        **Explicación teórica:**
        [Explicación clara y detallada adaptada al nivel {level}. Incluye definiciones, principios clave, y cómo se relaciona con {course_context}]

        💡 **Ejemplo práctico:**
        [Ejemplo específico conectado con los intereses: {', '.join(interests)}. Si los intereses incluyen 'tenis' y el concepto es sobre IA, da ejemplo de IA en análisis de partidos]

        🛠️ **Mini actividad práctica:**
        [Actividad inmediata para aplicar el concepto, también conectada con los intereses del usuario]

        CONTEXTO:
        - Módulo: {module_context}
        - Curso: {course_context}
        - Nivel: {level}
        - Intereses: {', '.join(interests)}

        REQUISITOS:
        - Máximo 1800 caracteres total
        - Lenguaje claro y adaptado al nivel
        - Ejemplos específicos con los intereses
        - Actividad práctica inmediata
        """
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Error generating concept content: {str(e)}")
            raise
    
    async def generate_module_content_chunked(
        self, 
        module_structure: Dict,
        course_context: str,
        level: CourseLevel,
        interests: List[str]
    ) -> List[ModuleChunk]:
        """Generate module content in optimized chunks"""
        
        chunks = []
        module_id = module_structure["module_id"]
        concepts = module_structure["concepts"]
        
        # Generate content for each concept
        for i, concept in enumerate(concepts):
            content = await self.generate_concept_content(
                concept,
                module_structure["title"],
                course_context,
                level,
                interests
            )
            
            chunk = ModuleChunk.create_chunk(
                content=content,
                order=i + 1,
                total=len(concepts) + 2,  # concepts + quiz + summary
                module_id=module_id
            )
            chunks.append(chunk)
        
        # Add quiz chunk
        quiz_content = f"""
        🧠 **Quiz del Módulo**
        
        Pregunta: {module_structure['quiz'][0]['question']}
        
        Opciones:
        A) {module_structure['quiz'][0]['options'][0]}
        B) {module_structure['quiz'][0]['options'][1]}
        C) {module_structure['quiz'][0]['options'][2]}
        D) {module_structure['quiz'][0]['options'][3]}
        
        💡 **Explicación:** {module_structure['quiz'][0]['explanation']}
        """
        
        quiz_chunk = ModuleChunk.create_chunk(
            content=quiz_content,
            order=len(concepts) + 1,
            total=len(concepts) + 2,
            module_id=module_id
        )
        chunks.append(quiz_chunk)
        
        # Add summary chunk
        summary_chunk = ModuleChunk.create_chunk(
            content=f"📋 **Resumen:** {module_structure['summary']}",
            order=len(concepts) + 2,
            total=len(concepts) + 2,
            module_id=module_id
        )
        chunks.append(summary_chunk)
        
        return chunks
    
    async def generate_final_project(
        self, 
        course_metadata: CourseMetadata,
        user_prompt: str,
        interests: List[str]
    ) -> FinalProject:
        """Generate final project based on course content and user interests"""
        
        prompt = f"""
        Crea un proyecto final para el curso "{course_metadata.title}" que integre todo el aprendizaje.
        Prompt original: {user_prompt}
        Intereses del usuario: {', '.join(interests)}
        Nivel: {course_metadata.level}
        
        Responde SOLO con JSON:
        {{
            "title": "Título del proyecto final",
            "description": "Descripción completa del proyecto (300-400 palabras)",
            "objectives": ["Objetivo 1", "Objetivo 2", "Objetivo 3"],
            "requirements": ["Requisito 1", "Requisito 2", "Requisito 3"],
            "deliverables": ["Entregable 1", "Entregable 2", "Entregable 3"],
            "evaluation_criteria": ["Criterio 1", "Criterio 2", "Criterio 3"],
            "estimated_hours": 12,
            "difficulty_level": "{course_metadata.level}",
            "resources": ["Recurso 1", "Recurso 2", "Recurso 3"]
        }}
        
        IMPORTANTE: Conecta el proyecto con los intereses {', '.join(interests)}
        """
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                project_dict = json.loads(json_match.group())
                return FinalProject(**project_dict)
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            logger.error(f"Error generating final project: {str(e)}")
            raise
    
    async def generate_course_summary(
        self, 
        course_metadata: CourseMetadata,
        modules: List[Module],
        interests: List[str]
    ) -> str:
        """Generate comprehensive course summary"""
        
        module_titles = [module.title for module in modules]
        
        prompt = f"""
        Genera un resumen completo para el curso "{course_metadata.title}".
        Módulos cubiertos: {', '.join(module_titles)}
        Intereses del usuario: {', '.join(interests)}
        
        Formato del resumen:
        
        🎓 **Resumen del Curso**
        
        📚 **Lo que has aprendido:**
        [Lista de conceptos principales cubiertos]
        
        🌟 **Habilidades desarrolladas:**
        [Lista de habilidades prácticas adquiridas]
        
        💡 **Aplicaciones prácticas:**
        [Cómo aplicar lo aprendido en contextos relacionados con {', '.join(interests)}]
        
        🚀 **Próximos pasos:**
        [Recomendaciones para continuar el aprendizaje]
        
        🎯 **Recursos adicionales:**
        [Lista de recursos para profundizar]
        
        Máximo 800 palabras total.
        """
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Error generating course summary: {str(e)}")
            raise 