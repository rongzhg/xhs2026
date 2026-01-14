@echo off
REM 小红书内容监控系统启动脚本 (Windows)

REM 创建虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt
pip install flask

REM 启动应用
echo 启动小红书内容监控系统...
python run.py

pause
