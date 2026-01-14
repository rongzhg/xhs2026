"""
API集成指南 - 如何集成外部视频/图片转文本API
"""

# ============ 集成示例1：调用本地API ============

EXAMPLE_1 = """
# 本地运行的转文本服务

# 启动Flask本地服务
from flask import Flask, request

app = Flask(__name__)

@app.route('/video-to-text', methods=['POST'])
def video_to_text():
    data = request.json
    video_url = data.get('video_url')
    
    # 调用你的视频处理库（如OpenAI Whisper）
    text = process_video(video_url)
    
    return {
        'code': 0,
        'text': text
    }

@app.route('/image-to-text', methods=['POST'])
def image_to_text():
    data = request.json
    image_url = data.get('image_url')
    
    # 调用OCR库（如Tesseract）
    text = ocr_image(image_url)
    
    return {
        'code': 0,
        'text': text
    }

# 在 xhs_monitor/converter.py 中配置：
# VIDEO_API_URL = "http://localhost:8000/video-to-text"
# IMAGE_API_URL = "http://localhost:8000/image-to-text"
"""


# ============ 集成示例2：调用云服务API ============

EXAMPLE_2 = """
# 集成阿里云视频理解服务

import requests
import json

class AlibabaVideoConverter:
    def __init__(self, access_key_id, access_key_secret, region_id='cn-shanghai'):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.region_id = region_id
        self.endpoint = f'videosearch.{region_id}.aliyuncs.com'
    
    def convert_video(self, content):
        '''调用阿里云视频理解API'''
        try:
            # 第一步：上传视频到OSS
            # ... OSS上传代码 ...
            
            # 第二步：调用视频理解API
            headers = self._build_headers()
            
            payload = {
                'VideoUrl': content.video_url,
                'VideoInfos': {
                    'MediaType': 'video',
                    'Duration': 300  # 示例
                }
            }
            
            response = requests.post(
                f'https://{self.endpoint}/api/analyze',
                json=payload,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                # 解析结果，提取文本
                content.converted_text = self._parse_result(result)
                content.conversion_status = 'completed'
                return True
            
            return False
            
        except Exception as e:
            print(f'Alibaba conversion error: {e}')
            return False
    
    def _build_headers(self):
        '''构建签名请求头'''
        # 实现签名逻辑...
        return {}
    
    def _parse_result(self, result):
        '''解析API返回结果'''
        # 提取视频中的文本、语音转文字等
        return result.get('text', '')
"""


# ============ 集成示例3：使用百度OCR API ============

EXAMPLE_3 = """
# 集成百度AI OCR服务

import requests
import base64

class BaiduOCRConverter:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = self._get_access_token()
    
    def _get_access_token(self):
        '''获取百度API的access_token'''
        url = 'https://aip.baidubce.com/oauth/2.0/token'
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }
        response = requests.get(url, params=params)
        return response.json().get('access_token')
    
    def convert_image(self, content):
        '''使用百度OCR进行图片转文本'''
        try:
            all_texts = []
            
            for image_url in content.img_urls[:5]:
                # 方式1：直接传URL
                text = self._ocr_by_url(image_url)
                if text:
                    all_texts.append(text)
            
            if all_texts:
                content.converted_text = '\\n\\n'.join(all_texts)
                content.conversion_status = 'completed'
                return True
            
            return False
            
        except Exception as e:
            print(f'Baidu OCR error: {e}')
            return False
    
    def _ocr_by_url(self, image_url):
        '''通过URL调用百度OCR'''
        request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        
        params = {
            'access_token': self.access_token,
            'image_url': image_url
        }
        
        response = requests.post(request_url, params=params)
        result = response.json()
        
        # 提取OCR结果中的文本
        words_result = result.get('words_result', [])
        text = ''.join([item['words'] for item in words_result])
        
        return text
"""


# ============ 集成示例4：使用OpenAI Whisper进行语音转文字 ============

EXAMPLE_4 = """
# 集成OpenAI Whisper服务

import requests
import os

class OpenAIWhisperConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = 'whisper-1'
    
    def convert_video(self, content):
        '''使用OpenAI Whisper将视频音轨转为文本'''
        try:
            # 第一步：下载视频文件
            video_path = self._download_video(content.video_url)
            
            # 第二步：提取音频
            audio_path = self._extract_audio(video_path)
            
            # 第三步：调用Whisper API
            with open(audio_path, 'rb') as audio_file:
                transcript = self._call_whisper_api(audio_file)
            
            # 清理临时文件
            os.remove(video_path)
            os.remove(audio_path)
            
            content.converted_text = transcript
            content.conversion_status = 'completed'
            return True
            
        except Exception as e:
            print(f'Whisper conversion error: {e}')
            content.conversion_status = 'failed'
            return False
    
    def _call_whisper_api(self, audio_file):
        '''调用OpenAI Whisper API'''
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        files = {
            'file': audio_file,
            'model': (None, self.model)
        }
        
        response = requests.post(
            'https://api.openai.com/v1/audio/transcriptions',
            files=files,
            headers=headers
        )
        
        result = response.json()
        return result.get('text', '')
    
    def _download_video(self, url):
        '''下载视频文件'''
        # 实现下载逻辑...
        pass
    
    def _extract_audio(self, video_path):
        '''使用ffmpeg提取视频音频'''
        # 实现音频提取逻辑...
        pass
"""


# ============ 集成示例5：Docker方式运行本地服务 ============

EXAMPLE_5 = """
# Dockerfile - 本地转文本服务

FROM python:3.9-slim

WORKDIR /app

# 安装依赖
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    tesseract-ocr \\
    && rm -rf /var/lib/apt/lists/*

# 复制应用
COPY . .

# 安装Python依赖
RUN pip install -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["python", "service.py"]


# requirements.txt
Flask==2.3.0
openai-whisper==20230124
Pillow==9.5.0
pytesseract==0.3.10
requests==2.31.0


# docker-compose.yml
version: '3'
services:
  xhs-monitor:
    build: .
    ports:
      - "5000:5000"
    environment:
      - VIDEO_API_URL=http://converter-service:8000/video-to-text
      - IMAGE_API_URL=http://converter-service:8000/image-to-text
  
  converter-service:
    build:
      context: ./converter-service
    ports:
      - "8000:8000"
    volumes:
      - ./converter-service:/app
"""


# ============ 配置方法总结 ============

CONFIGURATION_STEPS = """
1. 获取API密钥或部署服务

2. 配置环境变量（.env文件）：
   VIDEO_API_URL=your_video_api_endpoint
   IMAGE_API_URL=your_image_api_endpoint

3. 或直接在 xhs_monitor/converter.py 中配置：
   VIDEO_API_URL = "https://your-api.com/video"
   IMAGE_API_URL = "https://your-api.com/image"

4. 确保API返回格式一致：
   {
       "code": 0,
       "text": "转换后的文本"
   }

5. 根据需要创建自定义Converter类继承ContentConverter

6. 在 xhs_monitor/app.py 中替换转换器
"""


if __name__ == '__main__':
    print("小红书内容监控系统 - API集成指南\\n")
    print("选择一个集成方案并按照示例实施。\\n")
    print("推荐集成方案：")
    print("1. 本地服务（easiest）")
    print("2. 百度OCR（最便宜）")
    print("3. 阿里云视频理解（功能全面）")
    print("4. OpenAI Whisper（准确度最高）")
