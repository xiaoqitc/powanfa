@echo off
chcp 65001 >nul

REM 自动安装依赖
pip install -r requirements.txt

REM 后台启动可视化大屏服务
start /min python web_app.py

REM 启动工具箱
python hacker_toolbox.py

pause 