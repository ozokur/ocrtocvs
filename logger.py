"""
Loglama modülü
"""
import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FORMAT, LOG_FILE


def setup_logger(name):
    """
    Logger oluşturur ve yapılandırır
    
    Args:
        name: Logger adı
        
    Returns:
        logging.Logger: Yapılandırılmış logger
    """
    # Logger oluştur
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Eğer handler yoksa ekle
    if not logger.handlers:
        # Dosya handler
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file_path = os.path.join(log_dir, f"{timestamp}_{LOG_FILE}")
        
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # Handler'ları ekle
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

