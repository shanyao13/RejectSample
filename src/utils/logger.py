import logging
import os
from datetime import datetime
from config.constant import Constant

# 创建 logs 目录
log_dir = os.path.join(Constant.BASE_DIR, 'src/logs')
os.makedirs(log_dir, exist_ok=True)

# 日志文件路径
log_file = os.path.join(log_dir, 'reject_sample.log')

# 日志格式
log_format = '%(asctime)s [%(levelname)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'

# 创建 logger（单例）
logger = logging.getLogger('rejectSample')
logger.setLevel(logging.DEBUG)  # 设置最低日志等级

# 避免重复添加 handler
if not logger.handlers:

    # 控制台 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))

    # 文件 Handler
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))

    # 添加 Handler 到 logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
