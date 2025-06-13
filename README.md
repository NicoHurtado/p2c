# 🚀 Prompt2Course - Sistema Inteligente de Generación de Cursos

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Un sistema avanzado de generación de cursos educativos que crea contenido personalizado, extenso y de alta calidad usando inteligencia artificial, con optimización de recursos y escalabilidad para miles de usuarios simultáneos.

## 🌟 Características Principales

### ⚡ Generación Ultrarrápida
- **Respuesta inmediata**: Metadatos e introducción en menos de 3 segundos
- **Chunking inteligente**: División optimizada del contenido en fragmentos de máximo 2000 caracteres
- **Streaming en tiempo real**: Server-Sent Events para seguimiento de progreso en vivo

### 🧠 IA Optimizada
- **Claude 3 Sonnet**: Integración avanzada para generación de contenido inteligente
- **Prompts especializados**: Optimización específica para cada tipo de contenido
- **Cache inteligente**: Reutilización de respuestas similares para optimizar costos

### 📚 Personalización Avanzada
- **Conexión con intereses**: Cada concepto se relaciona con los intereses del usuario
- **Niveles adaptativos**: Principiante, intermedio y avanzado
- **Ejemplos contextualizados**: Casos prácticos específicos para cada usuario

### 🎥 Multimedia Integrada
- **YouTube automático**: Búsqueda e integración automática de videos educativos
- **Audio TTS**: Generación de audio con ElevenLabs para conceptos clave
- **S3 optimizado**: Almacenamiento escalable con CDN

### 🏗️ Arquitectura Escalable
- **MongoDB Atlas**: Base de datos distribuida con índices optimizados
- **Redis**: Cache distribuido para alta performance
- **Async/await**: Programación asíncrona para máxima concurrencia

## 📋 Estructura del Proyecto

```
prompt2courseV1/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── api/
│   │   ├── __init__.py
│   │   └── courses.py          # Endpoints de cursos
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuración y variables de entorno
│   │   └── database.py         # Gestión de MongoDB Atlas
│   ├── models/
│   │   ├── __init__.py
│   │   └── course.py           # Modelos de datos Pydantic
│   └── services/
│       ├── __init__.py
│       ├── claude_service.py   # Servicio de Claude AI
│       ├── youtube_service.py  # Integración con YouTube
│       ├── elevenlabs_service.py # Servicio de TTS
│       ├── cache_service.py    # Cache Redis
│       └── course_generator.py # Orquestador principal
├── requirements.txt            # Dependencias Python
├── env.example                 # Variables de entorno ejemplo
├── example_usage.py           # Ejemplos de uso
└── README.md                  # Documentación
```

## 🚀 Instalación Rápida

### 1. Clona el repositorio
```bash
git clone <repository-url>
cd prompt2courseV1
```

### 2. Instala dependencias
```bash
pip install -r requirements.txt
```

### 3. Configura variables de entorno
```bash
cp env.example .env
# Edita .env con tus credenciales
```

### 4. Ejecuta la aplicación
```bash
python -m uvicorn app.main:app --reload
```

## ⚙️ Configuración

### Variables de Entorno Requeridas

```env
# MongoDB Atlas
MONGODB_ATLAS_URI=mongodb+srv://user:pass@cluster.mongodb.net/prompt2course

# AI Services
CLAUDE_API_KEY=sk-ant-your-key
ELEVENLABS_API_KEY=your-elevenlabs-key

# YouTube API
YOUTUBE_DATA_API_KEY=your-youtube-key

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=your-bucket
AWS_REGION=us-east-1

# Redis
REDIS_URL=redis://localhost:6379

# Application
SECRET_KEY=your-secret-key
```

### Servicios Externos Necesarios

1. **MongoDB Atlas** - Base de datos principal
2. **Claude AI (Anthropic)** - Generación de contenido
3. **ElevenLabs** - Text-to-Speech
4. **YouTube Data API** - Búsqueda de videos
5. **AWS S3** - Almacenamiento de audio
6. **Redis** - Cache y optimización

## 📖 Uso de la API

### 1. Generar Curso (< 3 segundos)

```bash
curl -X POST "http://localhost:8000/api/courses/generate" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Quiero aprender inteligencia artificial para mis proyectos",
  "level": "principiante",
  "interests": ["deportes", "tenis", "videojuegos", "programación"]
}'
```

**Respuesta:**
```json
{
  "course_id": "uuid-del-curso",
  "metadata": {
    "title": "IA para Proyectos: De Videojuegos a Análisis Deportivo",
    "description": "Un curso completo que te enseñará IA desde cero...",
    "level": "principiante",
    "estimated_duration": 25,
    "total_modules": 8,
    "module_list": ["Introducción a la IA", "Machine Learning Básico", ...]
  },
  "status": "generating",
  "introduction_ready": true
}
```

### 2. Seguir Progreso en Tiempo Real

```javascript
const eventSource = new EventSource('/api/courses/stream/uuid-del-curso');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.event_type === 'module_ready') {
        console.log(`Módulo completado: ${data.data.module_title}`);
        console.log(`Progreso: ${data.data.progress}%`);
    }
    
    if (data.event_type === 'course_complete') {
        console.log('¡Curso completado!');
        eventSource.close();
    }
};
```

### 3. Obtener Curso Completo

```bash
curl "http://localhost:8000/api/courses/uuid-del-curso"
```

### 4. Generar Audio TTS

```bash
curl -X POST "http://localhost:8000/api/courses/uuid-del-curso/audio" \
-H "Content-Type: application/json" \
-d '{
  "text": "La inteligencia artificial es una rama de la informática...",
  "language": "es"
}'
```

## 🏗️ Arquitectura del Sistema

### Flujo de Generación Optimizado

```mermaid
graph TD
    A[Usuario envía prompt] --> B[Análisis inicial 0.5s]
    B --> C[Generación metadatos 1s]
    C --> D[Introducción inmediata 1.5s]
    D --> E[Respuesta < 3s]
    D --> F[Generación asíncrona]
    F --> G[Primer módulo completo]
    F --> H[Búsqueda videos relevantes]
    F --> I[Módulos restantes por chunks]
    F --> J[TTS conceptos clave]
    G --> K[Notificaciones SSE]
    H --> K
    I --> K
    J --> K
```

### Estructura de Datos

```mermaid
erDiagram
    Course {
        string id
        CourseMetadata metadata
        string user_prompt
        string user_level
        array user_interests
        string status
        datetime created_at
    }
    
    CourseMetadata {
        string title
        string description
        string level
        int estimated_duration
        array prerequisites
        int total_modules
        array module_list
        array topics
    }
    
    Module {
        string module_id
        string title
        string description
        string objective
        array concepts
        array chunks
        array quiz
        string summary
        string practical_exercise
    }
    
    ModuleChunk {
        string chunk_id
        string content
        int total_chunks
        int chunk_order
        string checksum
    }
    
    Course ||--|| CourseMetadata : contains
    Course ||--o{ Module : has
    Module ||--o{ ModuleChunk : contains
```

## 🎯 Ejemplos de Cursos Generados

### Entrada:
```json
{
  "prompt": "Quiero aprender inteligencia artificial para mis proyectos",
  "level": "principiante", 
  "interests": ["deportes", "tenis", "videojuegos", "programación"]
}
```

### Resultado:
- **Título**: "IA para Proyectos: De Videojuegos a Análisis Deportivo"
- **Módulos**: 8 módulos personalizados
- **Ejemplos**: Análisis de jugadas de tenis con IA, algoritmos para videojuegos
- **Videos**: Integración automática de tutoriales relevantes
- **Audio**: TTS para conceptos clave en español

## 🔧 Optimizaciones Implementadas

### Performance
- **Chunking inteligente**: Máximo 2000 caracteres por fragmento
- **Cache multinivel**: Redis para AI responses, video searches, cursos
- **Async processing**: Generación paralela de contenido
- **Connection pooling**: MongoDB y Redis optimizados

### Costos de IA
- **Reutilización de contexto**: Mantener contexto base entre chunks
- **Prompts optimizados**: Específicos y concisos para cada tarea
- **Cache inteligente**: Evitar regeneración de contenido similar
- **Batch processing**: Múltiples chunks en una llamada cuando es posible

### Escalabilidad
- **Microservicios**: Servicios independientes para cada integración
- **Event-driven**: SSE para comunicación en tiempo real
- **Stateless**: API sin estado para balanceadores de carga
- **Resource pooling**: Gestión eficiente de conexiones

## 📊 Métricas y Monitoreo

### Endpoints de Estadísticas

```bash
# Estadísticas generales
curl "http://localhost:8000/api/courses/stats/overview"

# Health check
curl "http://localhost:8000/health"
```

### Métricas Clave
- **Tiempo de respuesta inicial**: < 3 segundos
- **Throughput**: 1000+ cursos simultáneos
- **Cache hit rate**: > 80%
- **Uptime**: 99.9%

## 🧪 Testing

### Ejecutar Ejemplo
```bash
python example_usage.py
```

### Prueba Rápida con curl
```bash
# Health check
curl http://localhost:8000/health

# Generar curso de prueba
curl -X POST "http://localhost:8000/api/courses/generate" \
-H "Content-Type: application/json" \
-d '{"prompt": "Python básico", "level": "principiante", "interests": ["programación"]}'
```

## 🔒 Seguridad

- **Rate limiting**: Límites por usuario y endpoint
- **API keys**: Validación de credenciales externas
- **CORS**: Configuración restrictiva
- **Input validation**: Pydantic para validación de datos
- **Error handling**: Manejo seguro de excepciones

## 🌐 Deployment

### Docker (Recomendado)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables de Producción
```env
APP_ENV=production
LOG_LEVEL=WARNING
CORS_ORIGINS=["https://tu-dominio.com"]
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Roadmap

- [ ] **Versión 1.1**: Integración con GPT-4 como alternativa
- [ ] **Versión 1.2**: Generación de imágenes con DALL-E
- [ ] **Versión 1.3**: Exportación a PDF/SCORM
- [ ] **Versión 1.4**: Dashboard web completo
- [ ] **Versión 2.0**: Análisis de voz y video del usuario

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **Anthropic** por Claude AI
- **FastAPI** por el framework
- **MongoDB** por la base de datos
- **ElevenLabs** por TTS
- **YouTube** por la API de videos

---

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la [documentación](#-uso-de-la-api)
2. Ejecuta el [health check](#-testing)
3. Verifica las [variables de entorno](#-configuración)
4. Consulta los [logs](#-métricas-y-monitoreo)

**¿Necesitas ayuda?** Abre un issue en GitHub con:
- Descripción del problema
- Logs relevantes
- Configuración (sin credenciales)
- Pasos para reproducir

---

<div align="center">

**🚀 Prompt2Course - Transformando la educación con IA**

[Documentación](README.md) • [API Docs](http://localhost:8000/docs) • [Ejemplos](example_usage.py)

</div> 