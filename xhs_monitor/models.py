"""数据模型定义"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class Account:
    """小红书账号模型"""
    
    def __init__(self, account_id: str, username: str, user_id: str, cookie: str, a1: str = ""):
        self.account_id = account_id
        self.username = username
        self.user_id = user_id
        self.cookie = cookie
        self.a1 = a1
        self.created_at = datetime.now().isoformat()
        self.status = "active"
    
    def to_dict(self):
        return {
            "account_id": self.account_id,
            "username": self.username,
            "user_id": self.user_id,
            "cookie": self.cookie,
            "a1": self.a1,
            "created_at": self.created_at,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        account = cls(
            data["account_id"],
            data["username"],
            data["user_id"],
            data["cookie"],
            data.get("a1", "")
        )
        account.created_at = data.get("created_at", datetime.now().isoformat())
        account.status = data.get("status", "active")
        return account


class Content:
    """小红书内容模型"""
    
    def __init__(self, 
                 note_id: str,
                 title: str,
                 desc: str,
                 content_type: str,  # "video" or "image"
                 publish_time: int,
                 link: str,
                 user_id: str,
                 username: str,
                 img_urls: Optional[List[str]] = None,
                 video_url: Optional[str] = None):
        self.note_id = note_id
        self.title = title
        self.desc = desc
        self.content_type = content_type
        self.publish_time = publish_time
        self.link = link
        self.user_id = user_id
        self.username = username
        self.img_urls = img_urls or []
        self.video_url = video_url
        self.converted_text = None  # 转换后的文本
        self.conversion_status = "pending"  # pending, processing, completed, failed
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "note_id": self.note_id,
            "title": self.title,
            "desc": self.desc,
            "content_type": self.content_type,
            "publish_time": self.publish_time,
            "link": self.link,
            "user_id": self.user_id,
            "username": self.username,
            "img_urls": self.img_urls,
            "video_url": self.video_url,
            "converted_text": self.converted_text,
            "conversion_status": self.conversion_status,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        content = cls(
            data["note_id"],
            data["title"],
            data["desc"],
            data["content_type"],
            data["publish_time"],
            data["link"],
            data["user_id"],
            data["username"],
            data.get("img_urls", []),
            data.get("video_url")
        )
        content.converted_text = data.get("converted_text")
        content.conversion_status = data.get("conversion_status", "pending")
        content.created_at = data.get("created_at", datetime.now().isoformat())
        return content


class Database:
    """简单的JSON文件数据库"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.accounts_file = os.path.join(data_dir, "accounts.json")
        self.contents_file = os.path.join(data_dir, "contents.json")
        
        # 创建数据目录
        os.makedirs(data_dir, exist_ok=True)
        
        # 初始化文件
        if not os.path.exists(self.accounts_file):
            self._save_json(self.accounts_file, {})
        if not os.path.exists(self.contents_file):
            self._save_json(self.contents_file, {})
    
    def _load_json(self, filepath: str) -> Dict:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_json(self, filepath: str, data: Dict):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 账号管理
    def add_account(self, account: Account) -> bool:
        accounts = self._load_json(self.accounts_file)
        if account.account_id in accounts:
            return False
        accounts[account.account_id] = account.to_dict()
        self._save_json(self.accounts_file, accounts)
        return True
    
    def get_account(self, account_id: str) -> Optional[Account]:
        accounts = self._load_json(self.accounts_file)
        if account_id in accounts:
            return Account.from_dict(accounts[account_id])
        return None
    
    def get_all_accounts(self) -> List[Account]:
        accounts = self._load_json(self.accounts_file)
        return [Account.from_dict(data) for data in accounts.values()]
    
    def delete_account(self, account_id: str) -> bool:
        accounts = self._load_json(self.accounts_file)
        if account_id in accounts:
            del accounts[account_id]
            self._save_json(self.accounts_file, accounts)
            return True
        return False
    
    def update_account(self, account: Account) -> bool:
        accounts = self._load_json(self.accounts_file)
        if account.account_id in accounts:
            accounts[account.account_id] = account.to_dict()
            self._save_json(self.accounts_file, accounts)
            return True
        return False
    
    # 内容管理
    def add_content(self, content: Content) -> bool:
        contents = self._load_json(self.contents_file)
        if content.note_id in contents:
            return False
        contents[content.note_id] = content.to_dict()
        self._save_json(self.contents_file, contents)
        return True
    
    def get_content(self, note_id: str) -> Optional[Content]:
        contents = self._load_json(self.contents_file)
        if note_id in contents:
            return Content.from_dict(contents[note_id])
        return None
    
    def get_user_contents(self, user_id: str) -> List[Content]:
        contents = self._load_json(self.contents_file)
        user_contents = [
            Content.from_dict(data) 
            for data in contents.values() 
            if data["user_id"] == user_id
        ]
        # 按发布时间降序排序
        return sorted(user_contents, key=lambda x: x.publish_time, reverse=True)
    
    def get_contents_by_type(self, user_id: str, content_type: str) -> List[Content]:
        contents = self.get_user_contents(user_id)
        return [c for c in contents if c.content_type == content_type]
    
    def update_content(self, content: Content) -> bool:
        contents = self._load_json(self.contents_file)
        if content.note_id in contents:
            contents[content.note_id] = content.to_dict()
            self._save_json(self.contents_file, contents)
            return True
        return False
    
    def get_all_contents(self) -> List[Content]:
        contents = self._load_json(self.contents_file)
        return [Content.from_dict(data) for data in contents.values()]
