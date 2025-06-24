@echo off
chcp 65001 >nul
title 破万法工具箱 - 自动上传到GitHub

echo.
echo ========================================
echo    破万法工具箱 - 自动上传到GitHub
echo    目标仓库: https://github.com/xiaoqitc/powanfa
echo    作者：小白  微信：ccyuwu8888
echo ========================================
echo.

echo 正在自动上传到GitHub...
python auto_upload_github.py

echo.
echo 按任意键退出...
pause >nul 