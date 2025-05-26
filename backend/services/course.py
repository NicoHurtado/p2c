import httpx
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

async def request_course_generation(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Request course generation from external API
    
    Args:
        payload: Dictionary containing prompt, experience_level, personality, learning_style, intensity
        
    Returns:
        Generated course data from external API
        
    Raises:
        httpx.HTTPError: If the request fails
        Exception: For other unexpected errors
    """
    logger.info(f"Requesting course generation with payload: {payload}")
    
    try:
        # Configure timeouts for AI generation (can take 10-15 minutes)
        timeout_config = httpx.Timeout(
            connect=30.0,    # 30 seconds to connect
            read=900.0,      # 15 minutes to read response
            write=30.0,      # 30 seconds to write request
            pool=30.0        # 30 seconds to get connection from pool
        )
        
        async with httpx.AsyncClient(timeout=timeout_config) as client:
            logger.info("Sending request to external API...")
            
            response = await client.post(
                "http://localhost:8001/api/v1/generate-course", 
                json=payload,
                headers={
                    "Content-Type": "application/json"
                }
            )
            
            logger.info(f"External API response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Course generated successfully: {result.get('titulo', 'Unknown title')}")
                return result
            else:
                logger.error(f"External API error: {response.status_code} - {response.text}")
                response.raise_for_status()
                
    except httpx.TimeoutException as e:
        logger.error(f"Timeout while calling external API: {str(e)}")
        raise Exception("La generación del curso está tomando más tiempo del esperado. Esto es normal para cursos complejos. Por favor, espera un momento más o intenta con un curso más simple.")
    except httpx.ConnectError:
        logger.error("Connection error to external API")
        raise Exception("No se puede conectar con el servicio de generación de cursos. Verifica que esté ejecutándose en el puerto 8001.")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from external API: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 422:
            raise Exception("Los datos enviados no son válidos. Verifica que todos los campos estén correctos.")
        elif e.response.status_code == 500:
            raise Exception("Error interno en el servicio de generación de cursos. Por favor, intenta de nuevo más tarde.")
        else:
            raise Exception(f"Error del servicio externo: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Unexpected error in course generation: {str(e)}", exc_info=True)
        if "timeout" in str(e).lower():
            raise Exception("La generación del curso está tomando más tiempo del esperado. Esto puede suceder con cursos complejos. Por favor, intenta de nuevo.")
        raise Exception(f"Error inesperado al generar el curso: {str(e)}") 