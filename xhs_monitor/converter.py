"""内容转换模块 - 调用外部接口进行视频/图片转文本"""
import requests
from typing import Optional
from .models import Content


class ContentConverter:
    """内容转换器"""
    
    def __init__(self, video_api_url: str = "", image_api_url: str = ""):
        """
        初始化转换器
        
        Args:
            video_api_url: 视频转文本API地址
            image_api_url: 图片转文本API地址
        """
        self.video_api_url = video_api_url
        self.image_api_url = image_api_url
        self.timeout = 30
    
    def convert_content(self, content: Content) -> bool:
        """
        转换内容（视频或图片转文本）
        
        Args:
            content: 要转换的内容
            
        Returns:
            是否转换成功
        """
        if content.content_type == "video" and content.video_url:
            return self.convert_video(content)
        elif content.content_type == "image" and content.img_urls:
            return self.convert_image(content)
        else:
            # 文本内容无需转换
            content.converted_text = content.desc or content.title
            content.conversion_status = "completed"
            return True
    
    def convert_video(self, content: Content) -> bool:
        """
        将视频转换为文本
        
        Args:
            content: 内容对象，包含video_url
            
        Returns:
            转换是否成功
        """
        if not self.video_api_url:
            # 如果没有配置API，使用原始描述
            content.converted_text = content.desc or content.title
            content.conversion_status = "completed"
            return True
        
        try:
            content.conversion_status = "processing"
            
            # 调用外部视频转文本接口
            payload = {
                "video_url": content.video_url,
                "note_id": content.note_id
            }
            
            response = requests.post(
                self.video_api_url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") or result.get("code") == 0:
                    content.converted_text = result.get("text", "") or result.get("data", {}).get("text", "")
                    content.conversion_status = "completed"
                    return True
            
            # 转换失败，使用原始描述
            content.converted_text = content.desc or content.title
            content.conversion_status = "failed"
            return False
            
        except Exception as e:
            print(f"Error converting video {content.note_id}: {str(e)}")
            content.converted_text = content.desc or content.title
            content.conversion_status = "failed"
            return False
    
    def convert_image(self, content: Content) -> bool:
        """
        将图片转换为文本
        
        Args:
            content: 内容对象，包含img_urls
            
        Returns:
            转换是否成功
        """
        if not self.image_api_url:
            # 如果没有配置API，使用原始描述
            content.converted_text = content.desc or content.title
            content.conversion_status = "completed"
            return True
        
        try:
            content.conversion_status = "processing"
            
            # 调用外部图片转文本接口
            all_texts = []
            for img_url in content.img_urls[:5]:  # 最多处理5张图片
                payload = {
                    "image_url": img_url,
                    "note_id": content.note_id
                }
                
                response = requests.post(
                    self.image_api_url,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success") or result.get("code") == 0:
                        text = result.get("text", "") or result.get("data", {}).get("text", "")
                        if text:
                            all_texts.append(text)
            
            if all_texts:
                content.converted_text = "\n\n".join(all_texts)
                content.conversion_status = "completed"
                return True
            else:
                # 转换失败，使用原始描述
                content.converted_text = content.desc or content.title
                content.conversion_status = "failed"
                return False
                
        except Exception as e:
            print(f"Error converting image {content.note_id}: {str(e)}")
            content.converted_text = content.desc or content.title
            content.conversion_status = "failed"
            return False


class DummyConverter(ContentConverter):
    """虚拟转换器 - 用于演示，不实际调用外部接口"""
    
    def convert_video(self, content: Content) -> bool:
        """虚拟视频转文本"""
        content.converted_text = f"[视频转文本] {content.title}\n\n{content.desc}\n\n来自视频URL: {content.video_url}"
        content.conversion_status = "completed"
        return True
    
    def convert_image(self, content: Content) -> bool:
        """虚拟图片转文本"""
        img_count = len(content.img_urls)
        content.converted_text = f"[图片转文本] {content.title}\n\n{content.desc}\n\n包含{img_count}张图片的内容已转文本"
        content.conversion_status = "completed"
        return True
