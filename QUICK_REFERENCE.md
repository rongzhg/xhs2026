# 小红书内容监控系统 - 快速参考指南

## 📋 项目文件结构

```
xhs_monitor/
├── __init__.py              # 包初始化
├── app.py                   # Flask应用主文件 ⭐
├── config.py                # 配置文件
├── models.py                # 数据模型与数据库 ⭐
├── crawler.py               # 内容爬取模块 ⭐
├── converter.py             # 内容转换模块 ⭐
├── wsgi.py                  # WSGI配置（生产环境）
├── templates/
│   └── index.html           # 前端主页面 ⭐
├── static/
│   ├── css/
│   │   └── style.css        # 样式文件 ⭐
│   └── js/
│       └── app.js           # 前端脚本 ⭐
├── README.md                # 详细文档
└── data/                    # 数据目录
    ├── accounts.json        # 账号数据
    └── contents.json        # 内容数据

run.py                       # 应用启动脚本
start.bat                    # Windows启动脚本
start.sh                     # Linux/Mac启动脚本
examples_advanced.py         # 高级示例代码
API_INTEGRATION_GUIDE.md     # API集成指南
QUICK_REFERENCE.md           # 本文件
```

## 🚀 快速启动

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install flask requests lxml
python run.py
```

### Linux/Mac
```bash
python -m venv venv
source venv/bin/activate
pip install flask requests lxml
python run.py
```

访问: http://localhost:5000

## 📱 主要功能模块

### 1️⃣ 账号管理 (models.py)
```python
from xhs_monitor.models import Account, Database

# 创建账号
account = Account(
    account_id="user_001",
    username="昵称",
    user_id="user123",
    cookie="cookie...",
    a1="a1_value"
)

# 保存账号
db = Database()
db.add_account(account)
```

### 2️⃣ 内容爬取 (crawler.py)
```python
from xhs_monitor.crawler import ContentCrawler

crawler = ContentCrawler()
contents = crawler.fetch_user_content(account, "target_user_id")
# 返回 List[Content]
```

### 3️⃣ 内容转换 (converter.py)
```python
from xhs_monitor.converter import DummyConverter, ContentConverter

# 虚拟转换（演示）
converter = DummyConverter()

# 自定义转换
class MyConverter(ContentConverter):
    def convert_video(self, content):
        # 你的转换逻辑
        pass
    
    def convert_image(self, content):
        # 你的转换逻辑
        pass
```

### 4️⃣ 数据存储 (models.py)
```python
db = Database(data_dir='data')

# 账号操作
db.add_account(account)
db.get_all_accounts()
db.delete_account(account_id)

# 内容操作
db.add_content(content)
db.get_user_contents(user_id)
db.get_contents_by_type(user_id, 'video')
db.update_content(content)
```

## 🔌 API端点总览

### 账号管理
| 方法 | 端点 | 功能 |
|------|------|------|
| GET | `/api/accounts` | 获取所有账号 |
| POST | `/api/accounts` | 添加新账号 |
| DELETE | `/api/accounts/{id}` | 删除账号 |

### 内容管理
| 方法 | 端点 | 功能 |
|------|------|------|
| POST | `/api/fetch-content` | 爬取内容 |
| POST | `/api/convert-content/{id}` | 转换单条内容 |
| GET | `/api/contents/user/{id}` | 获取用户内容 |
| GET | `/api/contents/type` | 按类型筛选 |
| GET | `/api/contents/{id}` | 获取内容详情 |

### 统计
| 方法 | 端点 | 功能 |
|------|------|------|
| GET | `/api/statistics` | 获取统计数据 |

## 🎨 前端功能说明

### 仪表盘
- 显示账号数、内容数、转换统计
- 内容类型分布图表
- 转换状态分布图表

### 账号管理
- 添加新账号表单
- 账号列表（可删除）
- 实时数据刷新

### 内容管理
- 内容爬取工具
- 内容筛选（用户/类型/状态）
- 内容列表展示
- 详情查看和转换

## 🔧 关键配置

### 环境变量 (.env)
```env
VIDEO_API_URL=http://your-api/video-to-text
IMAGE_API_URL=http://your-api/image-to-text
FLASK_ENV=development
DEBUG=true
```

### Python配置 (config.py)
```python
DATA_DIR = 'data'              # 数据目录
VIDEO_API_URL = ''             # 视频转文本API
IMAGE_API_URL = ''             # 图片转文本API
FLASK_ENV = 'development'      # Flask环境
DEBUG = True                   # 调试模式
CRAWL_INTERVAL = 1             # 爬取间隔
REQUEST_TIMEOUT = 10           # 超时时间
```

## 📊 数据模型

### Account 账号
```python
{
    "account_id": "uuid",
    "username": "账号昵称",
    "user_id": "小红书用户ID",
    "cookie": "浏览器Cookie",
    "a1": "签名用a1值",
    "created_at": "2024-01-01T12:00:00",
    "status": "active"
}
```

### Content 内容
```python
{
    "note_id": "笔记ID",
    "title": "标题",
    "desc": "描述",
    "content_type": "video|image|text",
    "publish_time": 1234567890,
    "link": "https://xiaohongshu.com/...",
    "user_id": "博主用户ID",
    "username": "博主昵称",
    "img_urls": ["url1", "url2"],
    "video_url": "video_url",
    "converted_text": "转换后的文本",
    "conversion_status": "completed|pending|processing|failed",
    "created_at": "2024-01-01T12:00:00"
}
```

## 🛠️ 常见操作

### 添加账号
```python
# API方式
POST /api/accounts
{
    "username": "test_account",
    "user_id": "user123",
    "cookie": "a1=xxx; ...",
    "a1": "a1_value"
}
```

### 爬取内容
```python
# API方式
POST /api/fetch-content
{
    "account_id": "account_uuid",
    "user_id": "target_user_id"
}
```

### 查询内容
```python
# 获取用户所有内容
GET /api/contents/user/user123

# 按类型筛选
GET /api/contents/type?user_id=user123&type=video

# 查看详情
GET /api/contents/note_id_xxx
```

## 🌐 部署方式

### 本地开发
```bash
python run.py
```

### 生产部署（Gunicorn）
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 xhs_monitor.app:app
```

### Docker部署
```bash
docker build -t xhs-monitor .
docker run -p 5000:5000 xhs-monitor
```

## 🔐 安全建议

1. **Cookie管理**
   - 不要在代码中硬编码Cookie
   - 使用环境变量存储敏感信息
   - 定期更新Cookie

2. **API调用**
   - 添加请求验证
   - 使用HTTPS
   - 实现速率限制

3. **数据保护**
   - 备份数据文件
   - 定期清理旧数据
   - 加密存储敏感信息

## 📈 扩展建议

### 1. 使用数据库
```python
# 替换JSON为MySQL/MongoDB
from sqlalchemy import create_engine

class DatabaseSQL:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
```

### 2. 添加用户认证
```python
from flask_login import LoginManager
from flask_cors import CORS

CORS(app)
login_manager = LoginManager(app)
```

### 3. 实现WebSocket实时更新
```python
from flask_socketio import SocketIO
socketio = SocketIO(app)
```

### 4. 添加定时任务
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(auto_crawl, 'interval', hours=1)
scheduler.start()
```

## 🐛 故障排除

### 问题：无法连接API
- ✓ 检查网络连接
- ✓ 确认API地址正确
- ✓ 检查防火墙设置
- ✓ 查看API返回的错误信息

### 问题：爬取失败
- ✓ 验证Cookie是否过期
- ✓ 检查用户ID格式
- ✓ 查看XHS是否修改了API

### 问题：转换失败
- ✓ 检查外部API是否可用
- ✓ 验证媒体URL可访问
- ✓ 查看API返回格式

## 📚 文档索引

| 文件 | 说明 |
|------|------|
| [xhs_monitor/README.md](xhs_monitor/README.md) | 详细使用文档 |
| [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md) | API集成指南 |
| [examples_advanced.py](examples_advanced.py) | 高级示例代码 |

## 💡 提示

- 🎯 首次使用建议从仪表盘开始
- 🎯 使用虚拟转换器(DummyConverter)进行测试
- 🎯 查看浏览器控制台(F12)获取详细日志
- 🎯 定期备份data目录

## 🤝 贡献

欢迎提交Issue和Pull Request!

---

**最后更新**: 2024年1月  
**项目**: 小红书内容监控系统 v1.0
