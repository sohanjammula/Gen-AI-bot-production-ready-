from loguru import logger
import sys
from pathlib import Path

# Create logs directory if not exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

# Remove default logger
logger.remove()

# Console logger (clean and readable)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>"
)

# File logger (persistent logs)
logger.add(
    LOG_FILE,
    rotation="10 MB",      # rotate after 10MB
    retention="10 days",   # keep logs for 10 days
    compression="zip",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
)

def get_logger():
    """Return configured logger instance"""
    return logger