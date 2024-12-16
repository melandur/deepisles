import psutil
from loguru import logger


def check_device_space() -> None:
    """Check if there is enough space on the device"""
    free_space = psutil.disk_usage('.').free
    if free_space < 2e8:  # 200MB
        message = 'Not enough space on device. Please free up some space.'
        logger.warning(message)
        raise UserWarning(message)
