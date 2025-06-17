import logging
import aioboto3
import os
import json
from typing import Optional
from datetime import datetime
from ..core.config import get_settings

logger = logging.getLogger(__name__)

class S3Service:
    """Service for managing S3 file uploads and downloads"""
    
    def __init__(self):
        self.settings = get_settings()
        self.bucket_name = self.settings.aws_s3_bucket
        self.region = self.settings.aws_region
        
        # Configurar credenciales
        self.aws_access_key_id = self.settings.aws_access_key_id
        self.aws_secret_access_key = self.settings.aws_secret_access_key
        
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            logger.warning("AWS credentials not configured. S3 operations will fail.")
        
        if not self.bucket_name:
            logger.warning("AWS S3 bucket not configured. Using default bucket name.")
            self.bucket_name = "prompt2course-audio-files"
    
    async def upload_audio_file(
        self, 
        audio_data: bytes, 
        filename: str,
        content_type: str = "audio/mpeg"
    ) -> Optional[str]:
        """
        Sube un archivo de audio a S3 y retorna la URL pública
        """
        try:
            # Generar key único para S3
            timestamp = int(datetime.now().timestamp())
            s3_key = f"podcast-audio/{timestamp}_{filename}"
            
            logger.info(f"📤 Subiendo audio a S3: {s3_key}")
            
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('s3') as s3_client:
                # Subir archivo
                await s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=audio_data,
                    ContentType=content_type,
                    # Removido ACL por compatibilidad con buckets modernos
                    Metadata={
                        'uploaded_at': str(datetime.now()),
                        'file_type': 'podcast_audio'
                    }
                )
                
                # Generar URL prefirmada (válida por 24 horas)
                presigned_url = await self.generate_presigned_url_internal(s3_client, s3_key, 86400)
                
                if presigned_url:
                    logger.info(f"✅ Audio subido exitosamente con URL prefirmada")
                    return presigned_url
                else:
                    # Fallback a URL directa (puede no funcionar si bucket no es público)
                    s3_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
                    logger.warning(f"⚠️ Usando URL directa (puede requerir configuración pública): {s3_url}")
                    return s3_url
                
        except Exception as e:
            logger.error(f"❌ Error subiendo audio a S3: {str(e)}")
            return None
    
    async def delete_audio_file(self, s3_url: str) -> bool:
        """
        Elimina un archivo de audio de S3
        """
        try:
            # Extraer key de la URL
            s3_key = s3_url.split(f"{self.bucket_name}.s3.{self.region}.amazonaws.com/")[1]
            
            logger.info(f"🗑️ Eliminando audio de S3: {s3_key}")
            
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('s3') as s3_client:
                await s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=s3_key
                )
                
                logger.info(f"✅ Audio eliminado de S3: {s3_key}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error eliminando audio de S3: {str(e)}")
            return False
    
    async def check_bucket_exists(self) -> bool:
        """
        Verifica si el bucket de S3 existe
        """
        try:
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('s3') as s3_client:
                await s3_client.head_bucket(Bucket=self.bucket_name)
                return True
                
        except Exception as e:
            logger.error(f"❌ Bucket {self.bucket_name} no existe o no es accesible: {str(e)}")
            return False
    
    async def create_bucket_if_not_exists(self) -> bool:
        """
        Crea el bucket de S3 si no existe
        """
        try:
            if await self.check_bucket_exists():
                logger.info(f"✅ Bucket {self.bucket_name} ya existe")
                return True
            
            logger.info(f"🪣 Creando bucket S3: {self.bucket_name}")
            
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('s3') as s3_client:
                if self.region == 'us-east-1':
                    # us-east-1 no requiere LocationConstraint
                    await s3_client.create_bucket(Bucket=self.bucket_name)
                else:
                    await s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                
                # Configurar CORS para reproducción web
                cors_configuration = {
                    'CORSRules': [
                        {
                            'AllowedHeaders': ['*'],
                            'AllowedMethods': ['GET', 'HEAD'],
                            'AllowedOrigins': ['*'],
                            'MaxAgeSeconds': 3000
                        }
                    ]
                }
                
                await s3_client.put_bucket_cors(
                    Bucket=self.bucket_name,
                    CORSConfiguration=cors_configuration
                )
                
                # Configurar política del bucket para acceso público de lectura
                await self._configure_public_read_policy(s3_client)
                
                logger.info(f"✅ Bucket {self.bucket_name} creado exitosamente con acceso público")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error creando bucket: {str(e)}")
            return False 
    
    async def _configure_public_read_policy(self, s3_client):
        """Configura política de bucket para permitir lectura pública de archivos de audio"""
        try:
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{self.bucket_name}/podcast-audio/*"
                    }
                ]
            }
            
            await s3_client.put_bucket_policy(
                Bucket=self.bucket_name,
                Policy=json.dumps(bucket_policy)
            )
            
            logger.info(f"✅ Política de acceso público configurada para {self.bucket_name}")
            
        except Exception as e:
            logger.warning(f"⚠️ No se pudo configurar política pública: {str(e)}")
    
    async def configure_bucket_for_public_access(self) -> bool:
        """Configura el bucket existente para acceso público"""
        try:
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('s3') as s3_client:
                # Configurar CORS
                cors_configuration = {
                    'CORSRules': [
                        {
                            'AllowedHeaders': ['*'],
                            'AllowedMethods': ['GET', 'HEAD'],
                            'AllowedOrigins': ['*'],
                            'MaxAgeSeconds': 3000
                        }
                    ]
                }
                
                await s3_client.put_bucket_cors(
                    Bucket=self.bucket_name,
                    CORSConfiguration=cors_configuration
                )
                
                # Configurar política de acceso público
                await self._configure_public_read_policy(s3_client)
                
                logger.info(f"✅ Bucket {self.bucket_name} configurado para acceso público")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error configurando acceso público: {str(e)}")
            return False
    
    async def generate_presigned_url(self, s3_key: str, expiration: int = 3600) -> Optional[str]:
        """Genera una URL prefirmada para acceso temporal al archivo"""
        try:
            session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            )
            
            async with session.client('s3') as s3_client:
                presigned_url = await s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': s3_key},
                    ExpiresIn=expiration
                )
                
                logger.info(f"✅ URL prefirmada generada para {s3_key}")
                return presigned_url
                
        except Exception as e:
            logger.error(f"❌ Error generando URL prefirmada: {str(e)}")
            return None
    
    async def generate_presigned_url_internal(self, s3_client, s3_key: str, expiration: int = 3600) -> Optional[str]:
        """Genera una URL prefirmada usando un cliente S3 existente"""
        try:
            presigned_url = await s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            
            logger.info(f"✅ URL prefirmada generada para {s3_key} (válida por {expiration//3600}h)")
            return presigned_url
            
        except Exception as e:
            logger.error(f"❌ Error generando URL prefirmada interna: {str(e)}")
            return None