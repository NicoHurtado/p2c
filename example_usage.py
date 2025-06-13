#!/usr/bin/env python3
"""
Ejemplo de uso del Sistema de Generación de Cursos Inteligente

Este script demuestra cómo usar la API para:
1. Generar un curso personalizado
2. Seguir el progreso en tiempo real
3. Obtener el contenido completo
4. Generar audio TTS
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any


class Prompt2CourseClient:
    """Cliente para la API de Prompt2Course"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    async def generate_course(self, prompt: str, level: str, interests: list) -> Dict[str, Any]:
        """Generar un nuevo curso"""
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "prompt": prompt,
                "level": level,
                "interests": interests
            }
            
            async with session.post(
                f"{self.base_url}/api/courses/generate",
                json=payload
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def get_course(self, course_id: str) -> Dict[str, Any]:
        """Obtener curso completo"""
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/api/courses/{course_id}"
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def stream_progress(self, course_id: str):
        """Seguir progreso en tiempo real"""
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/api/courses/stream/{course_id}"
            ) as response:
                
                async for line in response.content:
                    if line:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith('data: '):
                            data = json.loads(line_str[6:])
                            yield data
    
    async def generate_audio(self, course_id: str, text: str) -> Dict[str, Any]:
        """Generar audio TTS"""
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "text": text,
                "language": "es"
            }
            
            async with session.post(
                f"{self.base_url}/api/courses/{course_id}/audio",
                json=payload
            ) as response:
                response.raise_for_status()
                return await response.json()


async def example_full_workflow():
    """Ejemplo completo de uso del sistema"""
    
    print("🚀 Iniciando ejemplo de Prompt2Course...")
    
    # Inicializar cliente
    client = Prompt2CourseClient()
    
    # 1. Generar curso
    print("\n📚 Paso 1: Generando curso...")
    
    course_request = {
        "prompt": "Quiero aprender inteligencia artificial para mis proyectos",
        "level": "principiante",
        "interests": ["deportes", "tenis", "videojuegos", "programación"]
    }
    
    print(f"Prompt: {course_request['prompt']}")
    print(f"Nivel: {course_request['level']}")
    print(f"Intereses: {', '.join(course_request['interests'])}")
    
    try:
        course_response = await client.generate_course(
            course_request["prompt"],
            course_request["level"],
            course_request["interests"]
        )
        
        course_id = course_response["course_id"]
        metadata = course_response["metadata"]
        
        print(f"\n✅ Curso generado exitosamente!")
        print(f"🆔 ID del curso: {course_id}")
        print(f"📖 Título: {metadata['title']}")
        print(f"⏱️ Duración estimada: {metadata['estimated_duration']} horas")
        print(f"📑 Módulos: {metadata['total_modules']}")
        
        # 2. Seguir progreso en tiempo real
        print(f"\n⏳ Paso 2: Siguiendo progreso en tiempo real...")
        
        async for event in client.stream_progress(course_id):
            if event.get("event") == "module_ready":
                data = event.get("data", {})
                print(f"  ✅ Módulo completado: {data.get('module_title')}")
                print(f"     Progreso: {data.get('progress', 0):.1f}%")
                
            elif event.get("event") == "course_complete":
                print(f"  🎉 ¡Curso completado!")
                break
                
            elif event.get("event") == "error":
                print(f"  ❌ Error: {event.get('data', {}).get('message')}")
                break
        
        # 3. Obtener curso completo
        print(f"\n📖 Paso 3: Obteniendo curso completo...")
        
        course = await client.get_course(course_id)
        
        print(f"📚 Curso: {course['metadata']['title']}")
        print(f"📝 Descripción: {course['metadata']['description'][:100]}...")
        print(f"📑 Módulos disponibles: {len(course.get('modules', []))}")
        
        # Mostrar estructura de módulos
        for i, module in enumerate(course.get('modules', [])[:3]):  # Primeros 3 módulos
            print(f"\n  📚 Módulo {i+1}: {module['title']}")
            print(f"     🎯 Objetivo: {module['objective'][:80]}...")
            print(f"     🧩 Conceptos: {len(module['concepts'])}")
            print(f"     📝 Chunks: {len(module['chunks'])}")
            print(f"     🎥 Videos: {len(module.get('resources', {}).get('videos', []))}")
        
        # 4. Generar audio para un concepto
        print(f"\n🔊 Paso 4: Generando audio TTS...")
        
        if course.get('modules'):
            first_module = course['modules'][0]
            if first_module.get('chunks'):
                first_chunk = first_module['chunks'][0]
                audio_text = first_chunk['content'][:200] + "..."
                
                print(f"Generando audio para: {audio_text[:50]}...")
                
                try:
                    audio_response = await client.generate_audio(course_id, audio_text)
                    print(f"✅ Audio generado: {audio_response.get('audio_url')}")
                except Exception as e:
                    print(f"❌ Error generando audio: {e}")
        
        print(f"\n🎉 ¡Ejemplo completado exitosamente!")
        print(f"🔗 Puedes acceder al curso en: http://localhost:8000/api/courses/{course_id}")
        
    except Exception as e:
        print(f"❌ Error durante el ejemplo: {e}")


async def example_quick_test():
    """Ejemplo rápido para pruebas"""
    
    print("🧪 Prueba rápida del sistema...")
    
    client = Prompt2CourseClient()
    
    try:
        # Generar curso simple
        course_response = await client.generate_course(
            "Aprende Python básico",
            "principiante",
            ["programación", "tecnología"]
        )
        
        course_id = course_response["course_id"]
        print(f"✅ Curso generado: {course_id}")
        
        # Esperar un poco y obtener el curso
        await asyncio.sleep(5)
        
        course = await client.get_course(course_id)
        print(f"📚 Título: {course['metadata']['title']}")
        print(f"📊 Estado: {course['status']}")
        print(f"📑 Módulos: {len(course.get('modules', []))}")
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")


async def main():
    """Función principal"""
    
    print("=" * 60)
    print("🚀 PROMPT2COURSE - SISTEMA DE GENERACIÓN DE CURSOS")
    print("=" * 60)
    
    while True:
        print("\nOpciones disponibles:")
        print("1. 📖 Ejemplo completo de uso")
        print("2. 🧪 Prueba rápida")
        print("3. ❌ Salir")
        
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == "1":
            await example_full_workflow()
        elif choice == "2":
            await example_quick_test()
        elif choice == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    # Verificar que aiohttp esté instalado
    try:
        import aiohttp
    except ImportError:
        print("❌ Error: Instala aiohttp con: pip install aiohttp")
        exit(1)
    
    # Ejecutar ejemplo
    asyncio.run(main()) 