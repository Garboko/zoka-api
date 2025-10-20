import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10_000_000,  
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    error_handler = RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=10_000_000,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    root_logger.addHandler(error_handler)
    
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)
    
    return root_logger

logger = setup_logging()