import pytest
from unittest.mock import Mock, patch, AsyncMock

class TestStorageService:
    
    @patch('app.services.storage.Minio')
    def test_upload_file_success(self, mock_minio):
        from app.services.storage import StorageService
        
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_minio.return_value = mock_client
        
        service = StorageService()
        
        file_data = b"test data"
        result = service.upload_file(file_data, "test.txt", "text/plain")
        
        assert result is not None
        assert "test.txt" in result
        mock_client.put_object.assert_called_once()
    
    @patch('app.services.storage.Minio')
    def test_upload_file_failure(self, mock_minio):
        from app.services.storage import StorageService
        from minio.error import S3Error
        
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_client.put_object.side_effect = S3Error(
            "Error", "test", "resource", "request_id", "host_id", "response"
        )
        mock_minio.return_value = mock_client
        
        service = StorageService()
        
        with pytest.raises(Exception):
            service.upload_file(b"data", "test.txt")

class TestEmailService:
    
    @pytest.mark.asyncio  
    @patch('app.services.email.FastMail')
    async def test_send_verification_email(self, mock_fastmail):
        from app.services.email import EmailService
        
        service = EmailService()
        service.enabled = True
        
        mock_mail = AsyncMock()
        service.fast_mail = mock_mail
        
        await service.send_verification_email(
            email="test@example.com",
            user_name="Test User",
            token="test_token_123"
        )
        
        mock_mail.send_message.assert_called_once()