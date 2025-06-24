@echo off
chcp 65001 >nul
title 破万法工具箱 - GitHub上传

echo.
echo ========================================
echo    破万法工具箱 - GitHub上传
echo    目标仓库: https://github.com/xiaoqitc/powanfa
echo    作者：小白  微信：ccyuwu8888
echo ========================================
echo.

echo 正在上传到GitHub仓库...
python upload_to_powanfa.py

echo.
echo 按任意键退出...
pause >nul 