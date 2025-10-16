from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, DateTime, ForeignKey, Enum, JSON, DECIMAL, Integer, Boolean, Index
from sqlalchemy.sql import func
from typing import Optional, Dict, Any, List
from app.database.session import Base
import enum
from datetime import datetime

class SubmissionStatus(enum.Enum):
    draft = "draft"
    submitted = "submitted"
    validated = "validated"
    rejected = "rejected"
    syncing = "syncing"  # Nouveau statut pour sync en cours

class SyncStatus(enum.Enum):
    synced = "synced"
    pending = "pending"
    error = "error"
    offline = "offline"

class Submission(Base):
    __tablename__ = "submissions"
    
    # Identifiants de base
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    form_id: Mapped[str] = mapped_column(String(36), ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    submitted_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Données du formulaire consolidées
    submission_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    """
    Structure JSON consolidée:
    {
        "form_version": "1.2.0",
        "responses": {
            "participant_name": "John Doe",
            "age": 25,
            "photo_field": "reference_to_media_file",
            "gps_location": {"lat": 12.34, "lng": 56.78}
        },
        "calculated_fields": {
            "total_score": 85,
            "completion_rate": 0.95
        },
        "validation_errors": [],
        "draft_data": {
            "auto_saved_at": "2024-01-15T10:30:00Z",
            "completion_percentage": 75
        }
    }
    """
    
    # Statut et dates
    status: Mapped[SubmissionStatus] = mapped_column(Enum(SubmissionStatus), nullable=False, default=SubmissionStatus.draft)
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    completed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    
    # Géolocalisation (conservée pour index spatial)
    latitude: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 8))
    longitude: Mapped[Optional[float]] = mapped_column(DECIMAL(11, 8))
    location_accuracy: Mapped[Optional[float]] = mapped_column(DECIMAL(8, 2))  # en mètres
    
    # Informations de synchronisation (remplace sync_status table)
    sync_info: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    """
    Structure pour synchronisation:
    {
        "device_id": "device_abc123",
        "device_info": {
            "platform": "android",
            "version": "11.0",
            "app_version": "2.1.0"
        },
        "sync_status": "synced",
        "last_sync_at": "2024-01-15T12:00:00Z",
        "sync_attempts": 1,
        "offline_duration": 3600,  // en secondes
        "network_info": {
            "type": "wifi",
            "strength": "strong"
        },
        "conflicts": [],
        "error_details": null
    }
    """
    
    # Métadonnées des fichiers média (remplace media_file table)
    media_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    """
    Structure pour fichiers média:
    {
        "files": [
            {
                "field_name": "participant_photo",
                "file_id": "file_xyz789",
                "original_name": "photo.jpg",
                "file_path": "/uploads/2024/01/abc123.jpg",
                "file_size": 2048576,
                "mime_type": "image/jpeg",
                "uploaded_at": "2024-01-15T10:45:00Z",
                "dimensions": {"width": 1920, "height": 1080},
                "thumbnail_path": "/thumbnails/abc123_thumb.jpg",
                "processing_status": "completed",
                "hash": "sha256:abc123...",
                "virus_scan": "clean"
            }
        ],
        "total_size": 2048576,
        "storage_provider": "local",
        "backup_status": "completed"
    }
    """
    
    # Données de chiffrement (remplace encrypted_submission table)
    encryption_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    """
    Structure pour chiffrement:
    {
        "is_encrypted": true,
        "algorithm": "AES-256-GCM",
        "key_id": "submission_key_456",
        "encrypted_fields": ["personal_id", "phone_number"],
        "encryption_metadata": {
            "iv": "base64_encoded_iv",
            "auth_tag": "base64_encoded_tag",
            "encrypted_at": "2024-01-15T10:30:00Z"
        },
        "compliance": {
            "gdpr_compliant": true,
            "retention_period": 2555,  // jours
            "anonymization_date": "2025-01-15T00:00:00Z"
        }
    }
    """
    
    # Métadonnées étendues
    meta_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    """
    Métadonnées générales:
    {
        "user_agent": "Mozilla/5.0...",
        "ip_address": "192.168.1.100",
        "session_id": "sess_abc123",
        "referrer": "https://example.com",
        "submission_time_ms": 45000,  // temps de remplissage
        "language": "fr",
        "timezone": "Europe/Paris",
        "quality_score": 0.95,
        "flags": ["verified", "high_quality"],
        "tags": ["survey_wave_1", "priority"],
        "custom_attributes": {}
    }
    """
    
    # Statistiques de qualité
    quality_score: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 2))  # 0.00 à 1.00
    completion_percentage: Mapped[int] = mapped_column(Integer, default=0)  # 0 à 100
    validation_errors_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Cycle de vie
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    archived_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    
    # Relations
    form = relationship("Form", back_populates="submissions")
    submitter = relationship("User", back_populates="submissions")
    
    # Index optimisés pour performance
    __table_args__ = (
        Index('idx_submission_form_status', 'form_id', 'status'),
        Index('idx_submission_submitter', 'submitted_by'),
        Index('idx_submission_date', 'submitted_at'),
        Index('idx_submission_location', 'latitude', 'longitude'),
        Index('idx_submission_sync', 'submitted_by', 'submitted_at'),  # Pour sync mobile
        Index('idx_submission_quality', 'quality_score', 'completion_percentage'),
        Index('idx_submission_updated', 'updated_at'),
        Index('idx_submission_form_date', 'form_id', 'submitted_at'),  # Pour analytics
    )
    
    @validates('submission_data')
    def validate_submission_data(self, key, submission_data):
        """Validation de la structure des données de soumission"""
        if not isinstance(submission_data, dict):
            raise ValueError("submission_data must be a dictionary")
        
        if 'responses' not in submission_data:
            raise ValueError("submission_data must contain 'responses'")
        
        return submission_data
    
    @validates('completion_percentage')
    def validate_completion_percentage(self, key, value):
        """Validation du pourcentage de completion"""
        if not 0 <= value <= 100:
            raise ValueError("completion_percentage must be between 0 and 100")
        return value
    
    @validates('quality_score')
    def validate_quality_score(self, key, value):
        """Validation du score de qualité"""
        if value is not None and not 0.0 <= value <= 1.0:
            raise ValueError("quality_score must be between 0.0 and 1.0")
        return value
    
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
    
    @property
    def is_complete(self) -> bool:
        return self.completion_percentage == 100 and self.status != SubmissionStatus.draft
    
    @property
    def has_media_files(self) -> bool:
        """Vérifie si la soumission contient des fichiers média"""
        if not self.media_metadata:
            return False
        return len(self.media_metadata.get('files', [])) > 0
    
    @property
    def is_encrypted(self) -> bool:
        """Vérifie si la soumission contient des données chiffrées"""
        if not self.encryption_data:
            return False
        return self.encryption_data.get('is_encrypted', False)
    
    @property
    def sync_status(self) -> str:
        """Statut de synchronisation actuel"""
        if not self.sync_info:
            return SyncStatus.synced.value
        return self.sync_info.get('sync_status', SyncStatus.synced.value)
    
    @property
    def device_id(self) -> Optional[str]:
        """ID de l'appareil ayant créé la soumission"""
        if not self.sync_info:
            return None
        return self.sync_info.get('device_id')
    
    @property
    def total_media_size(self) -> int:
        """Taille totale des fichiers média en bytes"""
        if not self.media_metadata:
            return 0
        return self.media_metadata.get('total_size', 0)
    
    def get_media_files(self) -> List[Dict[str, Any]]:
        """Récupère la liste des fichiers média"""
        if not self.media_metadata:
            return []
        return self.media_metadata.get('files', [])
    
    def get_response_value(self, field_name: str) -> Any:
        """Récupère la valeur d'un champ spécifique"""
        responses = self.submission_data.get('responses', {})
        return responses.get(field_name)
    
    def add_media_file(self, field_name: str, file_info: Dict[str, Any]) -> None:
        """Ajoute un fichier média à la soumission"""
        if not self.media_metadata:
            self.media_metadata = {'files': [], 'total_size': 0}
        
        self.media_metadata['files'].append({
            'field_name': field_name,
            'uploaded_at': datetime.utcnow().isoformat(),
            **file_info
        })
        
        # Met à jour la taille totale
        file_size = file_info.get('file_size', 0)
        self.media_metadata['total_size'] = self.media_metadata.get('total_size', 0) + file_size
    
    def update_sync_status(self, status: str, device_id: str, error_details: Optional[str] = None) -> None:
        """Met à jour le statut de synchronisation"""
        if not self.sync_info:
            self.sync_info = {}
        
        self.sync_info.update({
            'device_id': device_id,
            'sync_status': status,
            'last_sync_at': datetime.utcnow().isoformat(),
            'sync_attempts': self.sync_info.get('sync_attempts', 0) + 1,
            'error_details': error_details
        })
    
    def calculate_quality_score(self) -> float:
        """Calcule le score de qualité basé sur plusieurs critères"""
        score = 1.0
        
        # Réduction pour erreurs de validation
        if self.validation_errors_count > 0:
            score -= min(0.3, self.validation_errors_count * 0.1)
        
        # Réduction pour completion incomplète
        if self.completion_percentage < 100:
            score -= (100 - self.completion_percentage) / 100 * 0.4
        
        # Bonus pour données géolocalisées
        if self.latitude is not None and self.longitude is not None:
            score += 0.1
        
        return max(0.0, min(1.0, score))