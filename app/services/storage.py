from minio import Minio
from minio.error import S3Error
from io import BytesIO
from typing import Optional, List
from datetime import timedelta
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        try:
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_USE_SSL
            )
            self.bucket_name = settings.MINIO_BUCKET_NAME
            self._ensure_bucket_exists()
            logger.info(f"MinIO connected: {settings.MINIO_ENDPOINT}/{self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to initialize MinIO client: {e}", exc_info=True)
            raise
    
    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket '{self.bucket_name}' created successfully")
            else:
                logger.info(f"Bucket '{self.bucket_name}' already exists")
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {e}", exc_info=True)
            raise
    
    def upload_file(
        self, 
        file_data: bytes, 
        object_name: str, 
        content_type: str = "application/octet-stream"
    ) -> str:
        try:
            file_stream = BytesIO(file_data)
            file_size = len(file_data)
            
            self.client.put_object(
                self.bucket_name,
                object_name,
                file_stream,
                file_size,
                content_type=content_type
            )
            
            logger.info(f"File uploaded: {object_name} ({file_size} bytes)")
            return f"{self.bucket_name}/{object_name}"
            
        except S3Error as e:
            logger.error(f"Error uploading file {object_name}: {e}", exc_info=True)
            raise Exception("Failed to upload file. Please try again.")
        except Exception as e:
            logger.error(f"Unexpected error uploading file {object_name}: {e}", exc_info=True)
            raise Exception("Failed to upload file. Please try again.")
    
    def download_file(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            
            logger.info(f"File downloaded: {object_name} ({len(data)} bytes)")
            return data
            
        except S3Error as e:
            logger.error(f"Error downloading file {object_name}: {e}", exc_info=True)
            raise Exception("Failed to download file.")
        except Exception as e:
            logger.error(f"Unexpected error downloading file {object_name}: {e}", exc_info=True)
            raise Exception("Failed to download file.")
    
    def delete_file(self, object_name: str) -> bool:
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"File deleted: {object_name}")
            return True
        except S3Error as e:
            logger.error(f"Error deleting file {object_name}: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting file {object_name}: {e}", exc_info=True)
            return False
    
    def get_file_url(self, object_name: str, expires: int = 3600) -> str:
        try:
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=timedelta(seconds=expires)
            )
            url = url.replace(settings.MINIO_ENDPOINT, settings.MINIO_EXTERNAL_ENDPOINT)
            logger.debug(f"🔗 Generated URL for {object_name}")
            return url
        except S3Error as e:
            logger.error(f"Error generating URL for {object_name}: {e}", exc_info=True)
            raise Exception("Failed to generate file URL.")
    
    def file_exists(self, object_name: str) -> bool:
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error:
            return False
    
    def list_files(self, prefix: str = "") -> List[str]:
        try:
            objects = self.client.list_objects(
                self.bucket_name,
                prefix=prefix,
                recursive=True
            )
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logger.error(f"Error listing files with prefix {prefix}: {e}", exc_info=True)
            return []

storage_service = StorageService()