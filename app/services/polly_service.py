import logging
import aioboto3
import uuid
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from ..models.course import AudioResource
from ..core.config import get_settings
from .s3_service import S3Service

logger = logging.getLogger(__name__)

class PollyService:
    """Service for text-to-speech audio generation using Amazon Polly"""
    
    def __init__(self):
        self.settings = get_settings()
        self.region = self.settings.aws_region
        self.aws_access_key_id = self.settings.aws_access_key_id
        self.aws_secret_access_key = self.settings.aws_secret_access_key
        self.s3_service = S3Service()
        
        # Voces en español de Amazon Polly (compatibles con neural)
        self.spanish_voices = {
            'female': {
                'voice_id': 'Lucia',  # España, muy natural, soporta neural
                'name': 'María',
                'language': 'es-ES'
            },
            'male': {
                'voice_id': 'Enrique',  # España, muy natural, soporta neural
                'name': 'Carlos', 
                'language': 'es-ES'
            }
        }
        
        # Alternativas de voces disponibles
        self.available_voices = {
            'spanish_spain': {
                'female': ['Conchita', 'Lucia'],  # España
                'male': ['Enrique']
            },
            'spanish_mexico': {
                'female': ['Mia', 'Lupe'],  # México  
                'male': ['Miguel']
            },
            'spanish_us': {
                'female': ['Penelope'],  # Estados Unidos
                'male': []
            }
        }
    
    async def generate_podcast_audio(
        self, 
        podcast_script: str,
        course_id: str,
        user_id: str = "anonymous"
    ) -> Optional[str]:
        """
        Genera un podcast con dos locutores alternando líneas usando Polly
        """
        try:
            logger.info(f"🎙️ Generando podcast con Polly para curso {course_id}")
            
            # Dividir el script en diálogos
            dialogue_lines = self._parse_podcast_script(podcast_script)
            
            if not dialogue_lines:
                logger.error("No se pudieron extraer líneas de diálogo del script")
                return None
            
            # Generar audio para cada línea con Polly
            audio_segments = []
            for i, (speaker, text) in enumerate(dialogue_lines):
                voice_config = self.spanish_voices.get(speaker, self.spanish_voices['female'])
                
                logger.info(f"🎤 Generando audio {i+1}/{len(dialogue_lines)} - {voice_config['name']}: {text[:50]}...")
                
                audio_data = await self._generate_single_audio_polly(
                    text, 
                    voice_config['voice_id'],
                    voice_config['language']
                )
                
                if audio_data:
                    audio_segments.append(audio_data)
                else:
                    logger.error(f"Error generando segmento {i+1}")
            
            if not audio_segments:
                logger.error("No se pudieron generar segmentos de audio")
                return None
            
            # Combinar todos los segmentos
            combined_audio_data = await self._combine_audio_segments(audio_segments)
            
            if combined_audio_data:
                # Subir a S3
                filename = f"podcast_{course_id}_{int(datetime.now().timestamp())}.mp3"
                s3_url = await self.s3_service.upload_audio_file(
                    combined_audio_data, 
                    filename,
                    "audio/mpeg"
                )
                
                if s3_url:
                    logger.info(f"🎧 Podcast subido a S3: {s3_url}")
                    return s3_url
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error generando podcast con Polly: {str(e)}")
            return None
    
    def _parse_podcast_script(self, script: str) -> List[Tuple[str, str]]:
        """
        Parsea el script del podcast para extraer diálogos
        Formato esperado:
        MARÍA: Texto de la locutora
        CARLOS: Texto del locutor
        """
        lines = script.strip().split('\n')
        dialogue_lines = []
        current_speaker = 'female'  # Empezar con voz femenina
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detectar cambio de locutor
            if line.upper().startswith('MARÍA:') or line.upper().startswith('MARIA:'):
                current_speaker = 'female'
                text = line.split(':', 1)[1].strip()
            elif line.upper().startswith('CARLOS:'):
                current_speaker = 'male'
                text = line.split(':', 1)[1].strip()
            else:
                # Si no hay indicador, alternar automáticamente
                text = line
                current_speaker = 'male' if current_speaker == 'female' else 'female'
            
            if text:
                dialogue_lines.append((current_speaker, text))
        
        return dialogue_lines
    
    async def _generate_single_audio_polly(
        self, 
        text: str, 
        voice_id: str,
        language: str = 'es-ES'
    ) -> Optional[bytes]:
        """Genera audio para un segmento individual usando Amazon Polly"""
        try:
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('polly') as polly_client:
                # Intentar primero con engine neural, fallback a standard
                try:
                    response = await polly_client.synthesize_speech(
                        Text=text,
                        OutputFormat='mp3',
                        VoiceId=voice_id,
                        LanguageCode=language,
                        Engine='neural',  # Intentar neural para mejor calidad
                        SampleRate='22050'
                    )
                except Exception as neural_error:
                    if "engine is not supported" in str(neural_error).lower():
                        logger.warning(f"Neural engine no soportado, usando standard engine")
                        response = await polly_client.synthesize_speech(
                            Text=text,
                            OutputFormat='mp3',
                            VoiceId=voice_id,
                            LanguageCode=language,
                            Engine='standard',  # Fallback a standard
                            SampleRate='22050'
                        )
                    else:
                        raise neural_error
                
                # Leer el stream de audio
                audio_data = await response['AudioStream'].read()
                
                logger.info(f"✅ Audio generado con Polly: {len(audio_data)} bytes")
                return audio_data
                
        except Exception as e:
            logger.error(f"❌ Error generando audio con Polly: {str(e)}")
            return None
    
    async def _combine_audio_segments(self, audio_segments: List[bytes]) -> Optional[bytes]:
        """
        Combina segmentos de audio (concatenación simple)
        Para mejor calidad, se puede usar ffmpeg en el futuro
        """
        try:
            combined_audio = b''
            for segment in audio_segments:
                combined_audio += segment
            
            logger.info(f"🎧 Segmentos combinados: {len(combined_audio)} bytes totales")
            return combined_audio
            
        except Exception as e:
            logger.error(f"❌ Error combinando segmentos: {str(e)}")
            return None
    
    async def generate_audio_for_text(
        self, 
        text: str,
        user_id: str,
        voice_type: str = 'female',
        language: str = 'es-ES'
    ) -> Optional[AudioResource]:
        """Genera audio para texto simple usando Polly"""
        try:
            voice_config = self.spanish_voices.get(voice_type, self.spanish_voices['female'])
            
            audio_data = await self._generate_single_audio_polly(
                text, 
                voice_config['voice_id'],
                voice_config['language']
            )
            
            if audio_data:
                filename = f"audio_{uuid.uuid4()}.mp3"
                s3_url = await self.s3_service.upload_audio_file(
                    audio_data,
                    filename,
                    "audio/mpeg"
                )
                
                if s3_url:
                    return AudioResource(
                        original_text=text,
                        s3_url=s3_url,
                        language=language,
                        duration=None,  # Se puede calcular si es necesario
                        created_by=user_id
                    )
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error generando audio simple: {str(e)}")
            return None
    
    async def generate_audio_for_concept(
        self, 
        concept_content: str,
        user_id: str,
        concept_name: str
    ) -> Optional[AudioResource]:
        """Genera audio para un concepto específico"""
        return await self.generate_audio_for_text(
            concept_content,
            user_id,
            voice_type='female',
            language='es-ES'
        )
    
    async def test_polly_connection(self) -> bool:
        """Prueba la conexión con Amazon Polly"""
        try:
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('polly') as polly_client:
                # Listar voces disponibles para verificar conexión
                response = await polly_client.describe_voices(LanguageCode='es-ES')
                voices = response.get('Voices', [])
                
                logger.info(f"✅ Polly conectado. Voces en español disponibles: {len(voices)}")
                
                for voice in voices:
                    logger.info(f"   - {voice['Name']} ({voice['Gender']}) - {voice.get('LanguageName', 'N/A')}")
                
                return True
                
        except Exception as e:
            logger.error(f"❌ Error conectando con Polly: {str(e)}")
            return False
    
    async def list_available_voices(self, language_code: str = 'es-ES') -> List[Dict]:
        """Lista todas las voces disponibles en Polly para el idioma especificado"""
        try:
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('polly') as polly_client:
                response = await polly_client.describe_voices(LanguageCode=language_code)
                return response.get('Voices', [])
                
        except Exception as e:
            logger.error(f"❌ Error listando voces de Polly: {str(e)}")
            return [] 