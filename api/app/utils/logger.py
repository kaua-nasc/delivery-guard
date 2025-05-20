import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    """Configuração completa do sistema de logs"""
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger("deliveryguard")
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    file_handler = RotatingFileHandler(
        log_dir / "deliveryguard.log",
        maxBytes=1024 * 1024 * 5,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    class EndpointFilter(logging.Filter):
        def filter(self, record):
            return record.getMessage().find("/health") == -1
    
    access_logger = logging.getLogger("deliveryguard.access")
    access_logger.addFilter(EndpointFilter())
    
    return logger

# Uso recomendado:
# from app.utils.logger import setup_logging
# logger = setup_logging()