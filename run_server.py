#!/usr/bin/env python3
"""
Script para ejecutar el servidor Prompt2Course

Este script inicia el servidor FastAPI con la configuración optimizada
para desarrollo o producción.
"""

import sys
import os
import logging
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Configurar logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("prompt2course.log")
        ]
    )

def check_environment():
    """Verificar variables de entorno críticas"""
    required_vars = [
        "MONGODB_ATLAS_URI",
        "CLAUDE_API_KEY", 
        "SECRET_KEY"
    ]
    
    print("🔍 Verificando variables de entorno...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print(f"✅ Archivo .env encontrado: {env_file.absolute()}")
    else:
        print("❌ Archivo .env no encontrado")
        print("💡 Copia env.example a .env y configura las variables")
        sys.exit(1)
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Show partial value for verification (hide sensitive parts)
            if var == "SECRET_KEY":
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            elif var == "CLAUDE_API_KEY":
                display_value = f"{value[:12]}..." if len(value) > 12 else "***"
            else:
                display_value = f"{value[:20]}..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
    
    if missing_vars:
        print("\n❌ Variables de entorno faltantes:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Verifica que el archivo .env tenga estas variables configuradas")
        print("💡 Ejemplo:")
        print("   MONGODB_ATLAS_URI=mongodb+srv://user:pass@cluster.mongodb.net/...")
        print("   CLAUDE_API_KEY=sk-ant-...")
        print("   SECRET_KEY=tu-clave-secreta-larga")
        sys.exit(1)
    
    print("✅ Todas las variables de entorno están configuradas")

def main():
    """Función principal"""
    print("🚀 Iniciando Prompt2Course API...")
    
    # Setup logging
    setup_logging()
    
    # Debug mode to show .env content
    if "--debug-env" in sys.argv:
        print("\n🔍 DEBUG: Contenido del archivo .env:")
        try:
            with open(".env", "r") as f:
                for i, line in enumerate(f.readlines(), 1):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            # Hide sensitive values
                            if any(sensitive in key.upper() for sensitive in ["KEY", "SECRET", "PASSWORD"]):
                                display_value = "***HIDDEN***"
                            else:
                                display_value = value[:30] + "..." if len(value) > 30 else value
                            print(f"   Línea {i}: {key}={display_value}")
                        else:
                            print(f"   Línea {i}: {line}")
        except FileNotFoundError:
            print("   ❌ Archivo .env no encontrado")
        print()
    
    # Check environment
    if not os.getenv("SKIP_ENV_CHECK"):
        check_environment()
    
    # Get configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("APP_ENV", "development") == "development"
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    print(f"🌐 Host: {host}")
    print(f"🔌 Puerto: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"📊 Log Level: {log_level}")
    print("=" * 50)
    
    # Run server
    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 