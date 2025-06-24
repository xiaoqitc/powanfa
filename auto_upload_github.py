#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
破万法工具箱 - 自动上传到GitHub
作者：小白
功能：自动上传工具箱到GitHub仓库
"""

import os
import sys
import subprocess
import requests
import json
import webbrowser
from pathlib import Path

class AutoGitHubUploader:
    def __init__(self):
        self.repo_owner = "xiaoqitc"
        self.repo_name = "powanfa"
        self.repo_url = f"https://github.com/{self.repo_owner}/{self.repo_name}"
        self.current_dir = Path.cwd()
        
    def run_command(self, command, cwd=None):
        """执行命令并返回结果"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=cwd or self.current_dir
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def check_git_installed(self):
        """检查Git是否已安装"""
        print("=== 检查Git安装 ===")
        success, stdout, stderr = self.run_command("git --version")
        if success:
            print(f"✓ Git已安装: {stdout.strip()}")
            return True
        else:
            print("✗ Git未安装")
            print("正在打开Git下载页面...")
            webbrowser.open("https://git-scm.com/downloads")
            return False
    
    def setup_git_config(self):
        """设置Git配置"""
        print("\n=== 设置Git配置 ===")
        
        # 检查是否已配置
        success, stdout, stderr = self.run_command("git config --global user.name")
        if not success or not stdout.strip():
            print("需要设置Git用户名")
            name = input("请输入Git用户名 (默认: xiaoqitc): ").strip()
            if not name:
                name = "xiaoqitc"
            self.run_command(f'git config --global user.name "{name}"')
            print(f"✓ 设置Git用户名: {name}")
        
        success, stdout, stderr = self.run_command("git config --global user.email")
        if not success or not stdout.strip():
            print("需要设置Git邮箱")
            email = input("请输入Git邮箱: ").strip()
            if email:
                self.run_command(f'git config --global user.email "{email}"')
                print(f"✓ 设置Git邮箱: {email}")
        
        print("✓ Git配置完成")
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        print("\n=== 创建.gitignore文件 ===")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# 项目特定
passwords_top1000.txt
*.log
temp/
tmp/
"""
        
        gitignore_path = self.current_dir / ".gitignore"
        if not gitignore_path.exists():
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("✓ 创建.gitignore文件")
        else:
            print("✓ .gitignore文件已存在")
    
    def init_git_repo(self):
        """初始化Git仓库"""
        print("\n=== 初始化Git仓库 ===")
        
        # 检查是否已经是Git仓库
        if (self.current_dir / ".git").exists():
            print("✓ Git仓库已存在")
            return True
        
        # 初始化Git仓库
        success, stdout, stderr = self.run_command("git init")
        if success:
            print("✓ 初始化Git仓库成功")
            return True
        else:
            print(f"✗ 初始化Git仓库失败: {stderr}")
            return False
    
    def add_and_commit_files(self):
        """添加并提交文件"""
        print("\n=== 添加并提交文件 ===")
        
        # 添加所有文件
        success, stdout, stderr = self.run_command("git add .")
        if not success:
            print(f"✗ 添加文件失败: {stderr}")
            return False
        
        print("✓ 添加文件成功")
        
        # 提交文件
        commit_message = "feat: 破万法工具箱 v1.0.0 - 多功能加密解码分析工具"
        success, stdout, stderr = self.run_command(f'git commit -m "{commit_message}"')
        if success:
            print("✓ 提交文件成功")
            return True
        else:
            print(f"✗ 提交文件失败: {stderr}")
            return False
    
    def setup_remote_and_push(self):
        """设置远程仓库并推送"""
        print("\n=== 设置远程仓库并推送 ===")
        
        # 添加远程仓库
        remote_url = f"https://github.com/{self.repo_owner}/{self.repo_name}.git"
        success, stdout, stderr = self.run_command(f'git remote add origin {remote_url}')
        if not success:
            # 如果远程仓库已存在，尝试更新
            success, stdout, stderr = self.run_command(f'git remote set-url origin {remote_url}')
            if not success:
                print(f"✗ 设置远程仓库失败: {stderr}")
                return False
        
        print("✓ 设置远程仓库成功")
        
        # 推送到GitHub
        print("正在推送到GitHub...")
        success, stdout, stderr = self.run_command("git push -u origin main")
        if not success:
            # 尝试推送到master分支
            success, stdout, stderr = self.run_command("git push -u origin master")
        
        if success:
            print("✓ 推送到GitHub成功")
            return True
        else:
            print(f"✗ 推送到GitHub失败: {stderr}")
            return False
    
    def open_github_token_page(self):
        """打开GitHub Token页面"""
        print("\n=== GitHub Token 设置 ===")
        print("需要GitHub Token来上传代码")
        print("正在打开GitHub Token设置页面...")
        
        webbrowser.open("https://github.com/settings/tokens")
        
        print("\n请按照以下步骤操作:")
        print("1. 点击 'Generate new token (classic)'")
        print("2. 选择 'repo' 权限")
        print("3. 点击 'Generate token'")
        print("4. 复制生成的token")
        print("5. 回到此窗口继续")
        
        input("\n完成Token设置后，按回车键继续...")
    
    def run(self):
        """运行完整的自动上传流程"""
        print("=== 破万法工具箱 - 自动上传到GitHub ===")
        print(f"目标仓库: {self.repo_url}")
        print("作者：小白  微信：ccyuwu8888  QQ：154418587")
        print()
        
        # 1. 检查Git安装
        if not self.check_git_installed():
            print("\n请先安装Git，然后重新运行此脚本")
            input("按回车键退出...")
            return
        
        # 2. 设置Git配置
        self.setup_git_config()
        
        # 3. 创建.gitignore
        self.create_gitignore()
        
        # 4. 初始化Git仓库
        if not self.init_git_repo():
            input("按回车键退出...")
            return
        
        # 5. 添加并提交文件
        if not self.add_and_commit_files():
            input("按回车键退出...")
            return
        
        # 6. 打开GitHub Token页面
        self.open_github_token_page()
        
        # 7. 设置远程仓库并推送
        if self.setup_remote_and_push():
            print(f"\n=== 上传完成 ===")
            print(f"✓ 项目已成功上传到GitHub")
            print(f"✓ 仓库地址: {self.repo_url}")
            print(f"✓ 请访问上述地址查看您的项目")
            
            # 打开GitHub仓库页面
            print("\n正在打开GitHub仓库页面...")
            webbrowser.open(self.repo_url)
            
            print("\n感谢使用破万法工具！")
        else:
            print("\n✗ 上传失败，请检查网络连接和Token设置")
        
        input("\n按回车键退出...")

def main():
    uploader = AutoGitHubUploader()
    uploader.run()

if __name__ == "__main__":
    main() 