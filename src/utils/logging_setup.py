import logging
import logging.handlers
from config.config import LOG_CONFIG

def setup_logging():
    """Setup logging configuration for the application."""
    logger = logging.getLogger('waiis_automation')
    logger.setLevel(getattr(logging, LOG_CONFIG['level']))
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_CONFIG['filename'],
        maxBytes=LOG_CONFIG['max_bytes'],
        backupCount=LOG_CONFIG['backup_count']
    )
    file_handler.setLevel(getattr(logging, LOG_CONFIG['level']))
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(LOG_CONFIG['format'])
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger