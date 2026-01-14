#!/bin/bash
# 小红书内容监控系统启动脚本 (Linux/Mac)

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt
pip install flask

# 启动应用
echo "启动小红书内容监控系统..."
python run.py
