#!/bin/bash
# 小红书内容监控系统启动脚本 (Linux/Mac)

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════╗"
echo "║     🍰 小红书内容监控系统                  ║"
echo "║                                            ║"
echo "║  项目启动脚本 (Linux/Mac)                 ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

# 检查Python是否已安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 未安装${NC}"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

echo -e "${GREEN}✓ Python 已安装${NC}"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}创建虚拟环境...${NC}"
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
    else
        echo -e "${RED}✗ 虚拟环境创建失败${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ 虚拟环境已存在${NC}"
fi

# 激活虚拟环境
echo -e "${YELLOW}激活虚拟环境...${NC}"
source venv/bin/activate
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 虚拟环境激活成功${NC}"
else
    echo -e "${RED}✗ 虚拟环境激活失败${NC}"
    exit 1
fi

# 安装依赖
echo -e "${YELLOW}安装依赖包...${NC}"
pip install -q flask requests lxml

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 依赖包安装成功${NC}"
else
    echo -e "${RED}✗ 依赖包安装失败${NC}"
    exit 1
fi

# 创建数据目录
if [ ! -d "data" ]; then
    echo -e "${YELLOW}创建数据目录...${NC}"
    mkdir -p data
    echo -e "${GREEN}✓ 数据目录创建成功${NC}"
fi

# 启动应用
echo ""
echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo -e "${GREEN}启动小红书内容监控系统...${NC}"
echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}应用启动中，请等待...${NC}"
echo -e "${YELLOW}访问地址: http://localhost:5000${NC}"
echo ""

python run.py

# 应用停止后的提示
echo ""
echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo -e "${YELLOW}应用已停止${NC}"
echo -e "${BLUE}════════════════════════════════════════════${NC}"
