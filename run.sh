#!/bin/bash
echo "<<<< 开始运行定时任务脚本 >>>>"
cd ~/iMaoTai-reserve
# 安装依赖
echo "安装依赖..."
pip3 install --no-cache-dir -r requirements.txt
# 检查是否有log文件夹
if [ -d "log" ]; then
    echo "目录存在, 继续运行"
else
    echo "目录不存在, 创建log文件夹"
    mkdir log
fi
python3 main.py
echo "<<<< 定时任务脚本已运行结束 >>>> \n"