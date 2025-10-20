import pytest
from app.core.security import get_password_hash, verify_password, create_access_token, verify_token
from datetime import timedelta

class TestPasswordHashing:
    
    def test_password_hash_different_from_plain(self):
        password = "mysecretpassword"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > len(password)
    
    def test_same_password_different_hashes(self):
        password = "samepassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2  
    
    def test_verify_correct_password(self):
        password = "correctpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_wrong_password(self):
        password = "correctpassword"
        wrong = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong, hashed) is False

class TestJWTTokens:
    
    def test_create_token(self):
        user_id = "user123"
        token = create_access_token(data={"sub": user_id})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_valid_token(self):
        user_id = "user123"
        token = create_access_token(data={"sub": user_id})
        
        verified_user_id = verify_token(token)
        assert verified_user_id == user_id
    
    def test_verify_invalid_token(self):
        invalid_token = "invalid.token.here"
        
        verified_user_id = verify_token(invalid_token)
        assert verified_user_id is None
    
    def test_token_expiration(self):
        import time
        user_id = "user123"
        
        token = create_access_token(
            data={"sub": user_id},
            expires_delta=timedelta(seconds=1)
        )
        
        assert verify_token(token) == user_id
        
        time.sleep(2)
        
        assert verify_token(token) is None