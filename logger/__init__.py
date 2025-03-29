"""Logger module."""

from loguru import logger
import os
logs_dir:str = 'logs'

os.makedirs(logs_dir, exist_ok=True)

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "    
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
    )

def setup_logger(name: str):
    base_name = f'{logs_dir}\{name}'
    base_name += '_{time:YYYYMMDD}.log'
    logger.add(
        base_name, 
        format=logger_format,
        rotation='1 day', 
        retention='7 days', 
        level='DEBUG', 
        backtrace=True, 
        diagnose=True
        )
    return logger

__all__ = ['setup_logger', 'logger']