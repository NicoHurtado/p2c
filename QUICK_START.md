# 🚀 Quick Start - Prompt2Course

## ⚡ Inicio Rápido (5 minutos)

### 1. Configuración Inicial

```bash
# Clonar y entrar al directorio
cd prompt2courseV1

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
```

### 2. Configurar Credenciales Mínimas

Edita el archivo `.env` con estas variables **obligatorias**:

```env
# OBLIGATORIO - MongoDB Atlas (gratis)
MONGODB_ATLAS_URI=mongodb+srv://user:pass@cluster.mongodb.net/prompt2course

# OBLIGATORIO - Claude AI (Anthropic)
CLAUDE_API_KEY=sk-ant-your-key-here

# OBLIGATORIO - Aplicación
SECRET_KEY=your-secret-key-123456

# OPCIONAL - Para desarrollo local
REDIS_URL=redis://localhost:6379
```

### 3. Ejecutar con Docker (Recomendado)

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f prompt2course-api
```

### 4. Ejecutar sin Docker

```bash
# Instalar Redis localmente
# macOS: brew install redis && brew services start redis
# Ubuntu: sudo apt install redis-server
# Windows: Usar Docker o WSL

# Ejecutar servidor
python run_server.py
```

### 5. Probar la API

```bash
# Health check
curl http://localhost:8000/health

# Generar primer curso
curl -X POST "http://localhost:8000/api/courses/generate" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Quiero aprender Python para análisis de datos",
  "level": "principiante",
  "interests": ["deportes", "estadísticas", "programación"]
}'
```

### 6. Usar el Cliente Python

```bash
# Ejecutar ejemplo interactivo
python example_usage.py
```

## 📊 URLs Importantes

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Redis GUI**: http://localhost:8081 (solo con Docker)

## 🔧 Configuración Avanzada (Opcional)

Para funcionalidad completa, agrega estas APIs:

```env
# YouTube API (videos automáticos)
YOUTUBE_DATA_API_KEY=your-youtube-key

# ElevenLabs (audio TTS)
ELEVENLABS_API_KEY=your-elevenlabs-key

# AWS S3 (almacenamiento de audio)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=your-bucket
```

## 🎯 Primer Uso

1. **Generar curso** → Respuesta inmediata (< 3 segundos)
2. **Seguir progreso** → Abrir http://localhost:8000/docs
3. **Usar SSE endpoint** → `/api/courses/stream/{course_id}`
4. **Obtener curso completo** → GET `/api/courses/{course_id}`

## 🆘 Solución de Problemas

### Error de conexión a MongoDB
```bash
# Verificar URL en .env
echo $MONGODB_ATLAS_URI
```

### Error de Claude API
```bash
# Verificar API key
echo $CLAUDE_API_KEY
```

### Puerto ocupado
```bash
# Cambiar puerto
export PORT=8001
python run_server.py
```

### Redis no conecta
```bash
# Con Docker
docker-compose up redis -d

# Local
redis-server
```

## 📖 Siguiente Paso

Ver la [documentación completa](README.md) para:
- Arquitectura del sistema
- APIs avanzadas
- Optimizaciones de producción
- Casos de uso completos

---

**¿Todo funcionando?** 🎉 
¡Tu sistema está listo para generar cursos inteligentes! 