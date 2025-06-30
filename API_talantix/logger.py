import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name: str = 'api_export') -> logging.Logger:
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    file_handler = RotatingFileHandler(
        log_dir / 'api_export.log',
        maxBytes=5_000_000,
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_format)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 