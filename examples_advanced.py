"""
高级使用示例 - 如何集成自定义转换API
"""

from xhs_monitor.models import Database, Account
from xhs_monitor.crawler import ContentCrawler
from xhs_monitor.converter import ContentConverter


class CustomVideoConverter(ContentConverter):
    """自定义视频转换器 - 集成你的API"""
    
    def __init__(self, custom_api_key: str = ""):
        super().__init__()
        self.api_key = custom_api_key
    
    def convert_video(self, content):
        """
        自定义视频转换逻辑
        
        示例：集成第三方API（如OpenAI Whisper、阿里云等）
        """
        try:
            content.conversion_status = "processing"
            
            # 示例：调用阿里云视频理解API
            import requests
            
            payload = {
                "video_url": content.video_url,
                "api_key": self.api_key
            }
            
            response = requests.post(
                "https://api.aliyun.com/video-analysis",  # 示例API地址
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content.converted_text = result.get("transcript", "") or result.get("summary", "")
                content.conversion_status = "completed"
                return True
            
            content.conversion_status = "failed"
            return False
            
        except Exception as e:
            print(f"Video conversion error: {e}")
            content.conversion_status = "failed"
            return False


class CustomImageConverter(ContentConverter):
    """自定义图片转换器 - 集成你的OCR API"""
    
    def __init__(self, ocr_api_endpoint: str = ""):
        super().__init__()
        self.ocr_endpoint = ocr_api_endpoint
    
    def convert_image(self, content):
        """
        自定义图片转换逻辑
        
        示例：集成百度OCR、腾讯OCR等
        """
        try:
            import requests
            
            content.conversion_status = "processing"
            all_texts = []
            
            for img_url in content.img_urls[:10]:  # 最多处理10张
                # 调用OCR API
                response = requests.post(
                    self.ocr_endpoint,
                    json={
                        "image_url": img_url,
                        "language": "chinese"
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    text = result.get("text", "")
                    if text:
                        all_texts.append(text)
            
            if all_texts:
                content.converted_text = "\n\n".join(all_texts)
                content.conversion_status = "completed"
                return True
            
            content.conversion_status = "failed"
            return False
            
        except Exception as e:
            print(f"Image conversion error: {e}")
            content.conversion_status = "failed"
            return False


# ============ 使用示例 ============

def example_1_basic_usage():
    """示例1：基础使用 - 添加账号并爬取内容"""
    
    # 初始化数据库
    db = Database(data_dir='data')
    
    # 创建账号
    account = Account(
        account_id="user_001",
        username="我的小红书账号",
        user_id="user123456",
        cookie="a1=xxx; x-sign=yyy; ...",
        a1="a1_value"
    )
    
    # 保存账号
    db.add_account(account)
    
    # 爬取内容
    crawler = ContentCrawler()
    contents = crawler.fetch_user_content(account, "target_user_id")
    
    # 保存内容
    for content in contents:
        db.add_content(content)
    
    print(f"成功爬取 {len(contents)} 条内容")


def example_2_custom_converter():
    """示例2：使用自定义转换器"""
    
    db = Database(data_dir='data')
    
    # 使用自定义转换器
    converter = CustomVideoConverter(custom_api_key="your_api_key")
    
    # 获取所有内容并转换
    all_contents = db.get_all_contents()
    
    for content in all_contents:
        if content.conversion_status == "pending":
            converter.convert_content(content)
            db.update_content(content)
            print(f"已转换: {content.title}")


def example_3_batch_processing():
    """示例3：批量处理 - 处理多个博主"""
    
    db = Database(data_dir='data')
    crawler = ContentCrawler()
    converter = CustomImageConverter(ocr_api_endpoint="https://your-ocr-api.com/api")
    
    # 要爬取的博主列表
    target_users = [
        "user123",
        "user456",
        "user789"
    ]
    
    # 获取账号
    account = db.get_all_accounts()[0]
    
    # 依次爬取每个博主的内容
    for user_id in target_users:
        print(f"正在爬取用户 {user_id}...")
        contents = crawler.fetch_user_content(account, user_id)
        
        for content in contents:
            if db.add_content(content):  # 只处理新内容
                converter.convert_content(content)
                db.update_content(content)
        
        print(f"用户 {user_id} 爬取完成，共 {len(contents)} 条内容")


def example_4_data_export():
    """示例4：导出数据为CSV"""
    
    import csv
    from datetime import datetime
    
    db = Database(data_dir='data')
    
    # 导出所有内容
    contents = db.get_all_contents()
    
    filename = f"xhs_contents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'note_id', 'title', 'username', 'content_type',
            'publish_time', 'conversion_status', 'converted_text', 'link'
        ])
        writer.writeheader()
        
        for content in contents:
            writer.writerow({
                'note_id': content.note_id,
                'title': content.title,
                'username': content.username,
                'content_type': content.content_type,
                'publish_time': datetime.fromtimestamp(content.publish_time),
                'conversion_status': content.conversion_status,
                'converted_text': content.converted_text[:100] if content.converted_text else '',
                'link': content.link
            })
    
    print(f"数据已导出到 {filename}")


def example_5_filter_and_analyze():
    """示例5：筛选和分析数据"""
    
    db = Database(data_dir='data')
    
    # 获取特定用户的所有视频
    user_contents = db.get_user_contents("user123")
    videos = [c for c in user_contents if c.content_type == 'video']
    
    print(f"用户 user123 有 {len(videos)} 个视频")
    
    # 统计转换状态
    completed = sum(1 for c in user_contents if c.conversion_status == 'completed')
    pending = sum(1 for c in user_contents if c.conversion_status == 'pending')
    
    print(f"已转换: {completed}, 待转换: {pending}")
    
    # 找出最新的内容
    latest_content = max(user_contents, key=lambda c: c.publish_time) if user_contents else None
    if latest_content:
        print(f"最新内容: {latest_content.title} ({latest_content.publish_time})")


if __name__ == '__main__':
    print("小红书内容监控系统 - 高级示例\n")
    
    # 取消注释运行相应示例
    # example_1_basic_usage()
    # example_2_custom_converter()
    # example_3_batch_processing()
    # example_4_data_export()
    # example_5_filter_and_analyze()
    
    print("\n请根据需要调用对应的示例函数")
