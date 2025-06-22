import logging
import os
from datetime import datetime

def setup_logging():
    """Setup logging configuration for the MindEase backend"""
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler(f'logs/mindease_{datetime.now().strftime("%Y%m%d")}.log')  # Daily log file
        ]
    )
    
    # Set specific log levels for different modules
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('uvicorn.access').setLevel(logging.INFO)
    
    # Create logger for the application
    logger = logging.getLogger(__name__)
    logger.info("📝 Logging system initialized")
    
    return logger 