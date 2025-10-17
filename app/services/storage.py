from minio import Minio
from minio.error import S3Error
from io import BytesIO
from typing import Optional
import os
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created successfully")
        except S3Error as e:
            print(f"Error creating bucket: {e}")
    
    def upload_file(self, file_data: bytes, object_name: str, content_type: str = "application/octet-stream") -> str:
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
            
            return f"{self.bucket_name}/{object_name}"
        except S3Error as e:
            raise Exception(f"Error uploading file: {e}")
    
    def download_file(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            raise Exception(f"Error downloading file: {e}")
    
    def delete_file(self, object_name: str) -> bool:
        try:
            self.client.remove_object(self.bucket_name, object_name)
            return True
        except S3Error as e:
            print(f"Error deleting file: {e}")
            return False
    
    def get_file_url(self, object_name: str, expires: int = 3600) -> str:
        try:
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=expires
            )
            return url
        except S3Error as e:
            raise Exception(f"Error generating URL: {e}")
    
    def file_exists(self, object_name: str) -> bool:
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error:
            return False

storage_service = StorageService()