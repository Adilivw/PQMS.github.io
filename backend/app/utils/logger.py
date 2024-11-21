import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.INFO):
    """设置应用日志"""
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    
    handler = RotatingFileHandler(
        log_file, maxBytes=10000000, backupCount=10
    )
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# 创建日志目录
if not os.path.exists('logs'):
    os.mkdir('logs')

# 应用日志
app_logger = setup_logger('app', 'logs/app.log')
# 错误日志
error_logger = setup_logger('error', 'logs/error.log', logging.ERROR) 