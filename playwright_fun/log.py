---
created: '2024-04-28 '
---
import logging
async def logger(log_path):
    # 设置日志的配置信息
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('myapp.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(log_path)
    return logger

# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')
