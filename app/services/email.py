from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType, MultipartSubtypeEnum
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import List, Dict, Any
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        if not settings.MAIL_SERVER or settings.MAIL_SERVER == "":
            self.enabled = False
            logger.warning("Email service disabled: MAIL_SERVER not configured")
            return
        
        self.enabled = True
        
        try:
            self.conf = ConnectionConfig(
                MAIL_USERNAME=settings.MAIL_USERNAME,
                MAIL_PASSWORD=settings.MAIL_PASSWORD,
                MAIL_FROM=settings.MAIL_FROM,
                MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
                MAIL_PORT=settings.MAIL_PORT,
                MAIL_SERVER=settings.MAIL_SERVER,
                MAIL_STARTTLS=settings.MAIL_STARTTLS,
                MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
                USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
                VALIDATE_CERTS=settings.MAIL_VALIDATE_CERTS,
                TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates' / 'email'
            )
            
            self.fast_mail = FastMail(self.conf)
            
            template_dir = Path(__file__).parent.parent / 'templates' / 'email'
            self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
            
            logger.info(f"Email service enabled with server: {settings.MAIL_SERVER}:{settings.MAIL_PORT}")
        except Exception as e:
            self.enabled = False
            logger.error(f"Failed to initialize email service: {e}")
    
    async def send_email(
        self,
        subject: str,
        recipients: List[str],
        template_name: str,
        template_data: Dict[str, Any]
    ):
        if not self.enabled:
            logger.info(f"[EMAIL DISABLED] Would send to {recipients}: {subject}")
            logger.debug(f"Template: {template_name}, Data: {template_data}")
            return True
        
        try:
            template = self.jinja_env.get_template(template_name)
            html_content = template.render(**template_data)
            
            message = MessageSchema(
                subject=subject,
                recipients=recipients,
                body=html_content,
                subtype="html"
            )
            
            await self.fast_mail.send_message(message)
            logger.info(f"Email sent successfully to {recipients}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Error sending email to {recipients}: {e}")
            return False
    
    async def send_verification_email(self, email: str, user_name: str, token: str):
        verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        
        return await self.send_email(
            subject="Verify your email address",
            recipients=[email],
            template_name="verify_email.html",
            template_data={
                "user_name": user_name,
                "verification_link": verification_link
            }
        )
    
    async def send_password_reset_email(self, email: str, user_name: str, token: str):
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        
        return await self.send_email(
            subject="Reset your password",
            recipients=[email],
            template_name="password_reset.html",
            template_data={
                "user_name": user_name,
                "reset_link": reset_link
            }
        )
    
    async def send_welcome_email(self, email: str, user_name: str):
        return await self.send_email(
            subject="Welcome to Zoka!",
            recipients=[email],
            template_name="welcome.html",
            template_data={
                "user_name": user_name
            }
        )

email_service = EmailService()