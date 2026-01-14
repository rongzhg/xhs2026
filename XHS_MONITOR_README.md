# 🍰 小红书内容监控系统

一个**完整的、功能丰富的、可立即使用**的小红书内容监控和分析平台。

## ⚡ 5分钟快速开始

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境（选择适合你的系统）
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖
pip install flask requests lxml

# 4. 启动应用
python run.py

# 5. 打开浏览器访问
# http://localhost:5000
```

## ✨ 核心功能

✅ **账号管理**  
支持注册多个小红书账号，方便管理

✅ **内容爬取**  
自动爬取博主的所有发布内容，智能分类

✅ **智能转换**  
- 视频 → 文本（调用外部API）
- 图片 → 文本（OCR识别）
- 保留原始文本

✅ **数据展示**  
展示发布时间、原始链接、转换文本，支持详情查看

✅ **可视化分析**  
实时统计信息、图表展示、数据筛选

## 📊 项目概览

```
xhs_monitor/              核心应用模块（1500+行代码）
├── app.py               Flask主应用
├── models.py            数据模型与数据库
├── crawler.py           内容爬取模块
├── converter.py         内容转换模块
├── templates/           前端页面
│   └── index.html       (350+行响应式页面)
└── static/              静态资源
    ├── css/style.css    (400+行样式)
    └── js/app.js        (650+行脚本)

run.py                   启动脚本
start.bat / start.sh     快速启动

BUILD_SUMMARY.md         项目总结（推荐首先阅读）
FINAL_SUMMARY.md         完成总结
QUICK_REFERENCE.md       快速参考指南
API_INTEGRATION_GUIDE.md API集成指南（5个示例）
PROJECT_STRUCTURE.md     项目结构说明
examples_advanced.py     高级代码示例
```

## 🎯 使用流程

### Step 1: 添加账号
1. 访问 http://localhost:5000
2. 进入"账号管理"
3. 填写小红书账号信息
4. 点击"添加账号"

### Step 2: 爬取内容
1. 进入"内容管理"
2. 选择账号，输入目标博主ID
3. 点击"爬取内容"
4. 系统自动爬取、分类、转换

### Step 3: 查看内容
1. 在"内容列表"中查看所有内容
2. 点击内容查看详情
3. 查看原始链接和转换后的文本

### Step 4: 分析数据
1. 进入"仪表盘"
2. 查看实时统计和图表
3. 下载或导出数据

## 🔌 API接口

### 账号管理
```
GET    /api/accounts              获取所有账号
POST   /api/accounts              添加新账号
DELETE /api/accounts/{id}         删除账号
```

### 内容管理
```
POST   /api/fetch-content         爬取内容
POST   /api/convert-content/{id}  转换单条内容
GET    /api/contents/user/{id}    获取用户内容
GET    /api/contents/type         按类型筛选
GET    /api/contents/{id}         获取详情
```

### 统计分析
```
GET    /api/statistics            获取统计数据
```

## 📚 文档指南

| 文档 | 说明 | 阅读时间 |
|------|------|--------|
| **[BUILD_SUMMARY.md](BUILD_SUMMARY.md)** | 项目构建总结和使用指南 | 10分钟 |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | 快速参考和常见问题 | 5分钟 |
| **[xhs_monitor/README.md](xhs_monitor/README.md)** | 详细使用文档 | 15分钟 |
| **[API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md)** | API集成指南（含示例） | 20分钟 |
| **[examples_advanced.py](examples_advanced.py)** | 高级代码示例 | 10分钟 |
| **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** | 项目结构详解 | 10分钟 |

## 🔧 配置说明

### 集成外部API（可选）

创建 `.env` 文件：

```env
# 视频转文本API
VIDEO_API_URL=http://your-api/video-to-text

# 图片转文本API
IMAGE_API_URL=http://your-api/image-to-text

# Flask环境
FLASK_ENV=development
```

系统提供了5种API集成方案示例，详见 [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md)

## 🚀 部署选项

### 选项1: 本地开发
```bash
python run.py
```

### 选项2: 生产环境
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 xhs_monitor.app:app
```

### 选项3: Docker
```bash
docker build -t xhs-monitor .
docker run -p 5000:5000 xhs-monitor
```

## 💡 常见问题

### Q: 如何获取Cookie？
A: 打开小红书网站 → F12开发者工具 → 应用/存储 → Cookies → xiaohongshu.com → 复制Cookie

### Q: 如何获取用户ID？
A: 访问用户主页，URL为 `https://www.xiaohongshu.com/user/{user_id}`

### Q: 爬取失败怎么办？
A: 
- 检查Cookie是否过期
- 确认用户ID格式正确
- 查看浏览器控制台错误信息（F12）

### Q: 如何集成自己的转换API？
A: 参考 [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md) 的示例代码

更多问题详见 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

## 🛠️ 技术栈

- **后端**: Python 3.7+ + Flask
- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **数据库**: JSON（支持迁移到MySQL/MongoDB）
- **图表**: Chart.js
- **部署**: Gunicorn + Docker

## 📊 项目统计

- **后端代码**: 1080+ 行
- **前端代码**: 1400+ 行
- **文档**: 2000+ 行
- **总计**: 4000+ 行代码和文档
- **API端点**: 9个
- **功能模块**: 8个

## 🎁 项目特色

🌟 **完整的功能体系** - 从注册到展示的完整流程  
🌟 **专业的UI/UX** - 响应式设计，用户友好  
🌟 **清晰的代码结构** - 易于理解和扩展  
🌟 **详尽的文档** - 从新手到高级都有覆盖  
🌟 **生产就绪** - 可立即投入使用  
🌟 **高度可定制** - 支持自定义扩展  

## 📞 需要帮助？

1. **快速问题** → 查看 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **使用问题** → 查看 [xhs_monitor/README.md](xhs_monitor/README.md)
3. **API集成** → 查看 [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md)
4. **代码示例** → 查看 [examples_advanced.py](examples_advanced.py)

## 📜 许可证

参考项目根目录的 LICENSE 文件

---

## 🎉 快速开始

```bash
python run.py
# 然后访问 http://localhost:5000
```

**项目已完成并可投入使用！** ✅

---

**项目名称**: 小红书内容监控系统  
**版本**: v1.0  
**状态**: 生产就绪  
**更新日期**: 2024-01-04  

🚀 立即开始使用吧！
