"""
配置文件
"""
import os

# 数据目录
DATA_DIR = os.getenv('DATA_DIR', 'data')

# 外部API配置
VIDEO_API_URL = os.getenv('VIDEO_API_URL', '')  # 视频转文本API
IMAGE_API_URL = os.getenv('IMAGE_API_URL', '')  # 图片转文本API

# Flask配置
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'

# 爬取配置
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 1))  # 爬取间隔（秒）
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))  # 请求超时（秒）
