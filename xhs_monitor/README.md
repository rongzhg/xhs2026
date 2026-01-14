# 小红书内容监控系统 - 使用说明

## 功能概述

该系统提供了一个完整的小红书内容监控和分析平台，包括以下核心功能：

### 1. 账号管理
- **注册多个监控账号**：支持添加多个小红书账号用于爬取内容
- **账号查看和删除**：管理已注册的账号列表

### 2. 内容爬取
- **批量爬取博主内容**：指定博主账号，一键爬取其所有发布内容
- **内容分类**：自动根据内容类型分类（视频、图片、文字）
- **内容去重**：避免重复爬取相同内容

### 3. 智能转换
- **视频转文本**：调用外部接口将视频内容转换为文本
- **图片转文本**：调用外部接口进行OCR识别，提取图片文字
- **文字保留**：纯文字内容直接保存
- **批量转换**：支持一键转换所有待处理内容

### 4. 数据展示
- **仪表盘**：实时统计数据（账号数、内容数、转换状态）
- **内容列表**：展示所有内容的发布时间、原始链接、预览文本
- **详细信息**：查看单条内容的完整信息，包括原始链接、转换后文本
- **智能筛选**：按博主、内容类型、转换状态进行筛选

## 快速开始

### 环境要求
- Python 3.7+
- pip

### 安装步骤

1. **克隆或进入项目目录**
```bash
cd xhs2026
```

2. **安装依赖**
```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
pip install flask
```

3. **启动应用**
```bash
# Windows:
python run.py
# 或使用启动脚本:
start.bat

# Linux/Mac:
python run.py
# 或使用启动脚本:
bash start.sh
```

4. **访问应用**
打开浏览器，访问 `http://localhost:5000`

## 使用指南

### 步骤1：添加监控账号

1. 进入"账号管理"标签页
2. 填写以下信息：
   - **账号昵称**：给账号起一个易识别的名称
   - **用户ID**：小红书账号的用户ID（从URL中获取）
   - **Cookie**：账号的Cookie（从浏览器开发者工具中获取）
   - **a1值**（可选）：用于签名的a1值
3. 点击"添加账号"按钮

#### 如何获取Cookie和用户ID？

**获取用户ID：**
- 登录小红书网站
- 访问自己或目标博主的个人主页
- URL格式为：`https://www.xiaohongshu.com/user/xxxxxx`
- `xxxxxx` 就是用户ID

**获取Cookie：**
- 打开浏览器开发者工具（F12）
- 进入"应用"/"存储" → "Cookies"
- 查找小红书域名 `xiaohongshu.com`
- 复制全部Cookie内容

### 步骤2：爬取内容

1. 进入"内容管理"标签页
2. 在"爬取内容"卡片中：
   - 选择要使用的账号
   - 输入目标博主的用户ID
3. 点击"爬取内容"按钮
4. 系统会自动：
   - 爬取该博主的所有发布内容
   - 识别内容类型（视频/图片/文字）
   - 触发转换流程

### 步骤3：查看和转换内容

1. 在"内容列表"中查看所有爬取的内容
2. 使用筛选功能：
   - 按博主筛选
   - 按内容类型筛选（视频/图片/文字）
   - 按转换状态筛选（已转换/待转换/失败）
3. 点击内容卡片或"查看"按钮查看详情
4. 在详情页面中：
   - 查看原始信息和媒体内容
   - 查看转换后的文本
   - 点击"转换文本"按钮重新转换
   - 点击"访问原始链接"查看小红书原文

### 步骤4：数据分析

在"仪表盘"标签页中：
- 查看监控账号总数
- 查看爬取的总内容数
- 查看已转换和待转换的内容统计
- 查看内容类型分布图表
- 查看转换状态分布图表

## 配置外部接口

系统支持集成外部的视频/图片转文本API。

### 配置方式

创建 `.env` 文件（在项目根目录）：

```env
# 视频转文本API地址
VIDEO_API_URL=https://your-api.com/video-to-text

# 图片转文本API地址
IMAGE_API_URL=https://your-api.com/image-to-text

# 爬取间隔（秒）
CRAWL_INTERVAL=1

# 请求超时（秒）
REQUEST_TIMEOUT=10

# Flask环境
FLASK_ENV=production
```

### API接口规范

**视频转文本接口：**
```json
POST /video-to-text
{
    "video_url": "视频URL",
    "note_id": "笔记ID"
}

返回：
{
    "code": 0,
    "text": "转换后的文本"
}
```

**图片转文本接口：**
```json
POST /image-to-text
{
    "image_url": "图片URL",
    "note_id": "笔记ID"
}

返回：
{
    "code": 0,
    "text": "转换后的文字"
}
```

## 数据存储

系统使用JSON文件进行数据存储，位置为 `data/` 目录：

- `data/accounts.json` - 存储所有添加的账号信息
- `data/contents.json` - 存储所有爬取的内容

## API接口文档

### 账号管理接口

**获取所有账号**
```
GET /api/accounts
```

**添加新账号**
```
POST /api/accounts
Content-Type: application/json

{
    "username": "账号昵称",
    "user_id": "用户ID",
    "cookie": "Cookie内容",
    "a1": "a1值（可选）"
}
```

**删除账号**
```
DELETE /api/accounts/{account_id}
```

### 内容管理接口

**爬取内容**
```
POST /api/fetch-content
Content-Type: application/json

{
    "account_id": "账号ID",
    "user_id": "目标用户ID"
}
```

**转换单条内容**
```
POST /api/convert-content/{note_id}
```

**获取用户内容**
```
GET /api/contents/user/{user_id}
```

**获取内容详情**
```
GET /api/contents/{note_id}
```

**按类型筛选内容**
```
GET /api/contents/type?user_id={user_id}&type={type}
```

### 统计接口

**获取统计数据**
```
GET /api/statistics
```

返回：
```json
{
    "code": 0,
    "data": {
        "total_accounts": 1,
        "total_contents": 100,
        "content_types": {
            "video": 30,
            "image": 50,
            "text": 20
        },
        "conversion_status": {
            "completed": 80,
            "pending": 20,
            "failed": 0
        }
    }
}
```

## 常见问题

### Q: 如何更新爬取的内容？
A: 重复执行"爬取内容"操作，系统会自动识别新内容并更新。

### Q: 转换失败了怎么办？
A: 
1. 检查是否配置了外部API
2. 点击"转换文本"按钮重试
3. 如果API地址不存在，系统会使用原始描述作为转换结果

### Q: 数据会被保存吗？
A: 是的，所有数据都会保存在 `data/` 目录下的JSON文件中

### Q: 如何删除某条内容？
A: 目前不支持直接删除，但可以删除整个账号，这样会删除该账号爬取的所有内容

## 扩展和定制

### 替换数据存储
编辑 `xhs_monitor/models.py` 中的 `Database` 类，可以将JSON存储替换为数据库（MySQL、MongoDB等）

### 添加新的转换方式
编辑 `xhs_monitor/converter.py`，继承 `ContentConverter` 类并实现自己的转换逻辑

### 定制UI样式
编辑 `xhs_monitor/static/css/style.css` 来修改页面样式

## 项目结构

```
xhs_monitor/
├── __init__.py
├── app.py              # Flask应用程序
├── config.py           # 配置文件
├── models.py           # 数据模型和数据库
├── crawler.py          # 内容爬取模块
├── converter.py        # 内容转换模块
├── templates/
│   └── index.html      # 主页面
└── static/
    ├── css/
    │   └── style.css   # 样式文件
    └── js/
        └── app.js      # 前端脚本
```

## 许可证

参考项目根目录的 LICENSE 文件

## 支持

如有问题，请提交Issue或联系开发者。
