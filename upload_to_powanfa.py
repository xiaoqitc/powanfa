#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
破万法工具箱 - GitHub上传脚本
专门用于上传到 https://github.com/xiaoqitc/powanfa
作者：小白
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

class PowanfaUploader:
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
        success, stdout, stderr = self.run_command("git --version")
        if success:
            print(f"✓ Git已安装: {stdout.strip()}")
            return True
        else:
            print("✗ Git未安装，请先安装Git")
            return False
    
    def check_git_configured(self):
        """检查Git配置"""
        success, stdout, stderr = self.run_command("git config --global user.name")
        if not success or not stdout.strip():
            print("✗ Git用户名未配置")
            name = input("请输入Git用户名: ")
            self.run_command(f'git config --global user.name "{name}"')
        
        success, stdout, stderr = self.run_command("git config --global user.email")
        if not success or not stdout.strip():
            print("✗ Git邮箱未配置")
            email = input("请输入Git邮箱: ")
            self.run_command(f'git config --global user.email "{email}"')
        
        print("✓ Git配置完成")
    
    def create_gitignore(self):
        """创建.gitignore文件"""
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
    
    def add_files(self):
        """添加文件到Git"""
        success, stdout, stderr = self.run_command("git add .")
        if success:
            print("✓ 添加文件到Git成功")
            return True
        else:
            print(f"✗ 添加文件失败: {stderr}")
            return False
    
    def commit_files(self, message="Initial commit"):
        """提交文件"""
        success, stdout, stderr = self.run_command(f'git commit -m "{message}"')
        if success:
            print("✓ 提交文件成功")
            return True
        else:
            print(f"✗ 提交文件失败: {stderr}")
            return False
    
    def add_remote(self):
        """添加远程仓库"""
        remote_url = f"https://github.com/{self.repo_owner}/{self.repo_name}.git"
        success, stdout, stderr = self.run_command(f'git remote add origin {remote_url}')
        if success:
            print("✓ 添加远程仓库成功")
            return True
        else:
            # 如果远程仓库已存在，尝试更新
            success, stdout, stderr = self.run_command(f'git remote set-url origin {remote_url}')
            if success:
                print("✓ 更新远程仓库地址成功")
                return True
            else:
                print(f"✗ 添加远程仓库失败: {stderr}")
                return False
    
    def push_to_github(self):
        """推送到GitHub"""
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
    
    def get_github_token(self):
        """获取GitHub Token"""
        print("\n=== GitHub Token 设置 ===")
        print("1. 访问 https://github.com/settings/tokens")
        print("2. 点击 'Generate new token (classic)'")
        print("3. 选择 'repo' 权限")
        print("4. 复制生成的token")
        print()
        
        token = input("请输入GitHub Token: ").strip()
        if not token:
            print("✗ Token不能为空")
            return None
        return token
    
    def run(self):
        """运行完整的GitHub上传流程"""
        print("=== 破万法工具箱 - GitHub上传 ===")
        print(f"目标仓库: {self.repo_url}")
        print("作者：小白  微信：ccyuwu8888  QQ：154418587")
        print()
        
        # 1. 检查Git安装
        if not self.check_git_installed():
            return
        
        # 2. 检查Git配置
        self.check_git_configured()
        
        # 3. 创建.gitignore
        self.create_gitignore()
        
        # 4. 初始化Git仓库
        if not self.init_git_repo():
            return
        
        # 5. 添加文件
        if not self.add_files():
            return
        
        # 6. 提交文件
        commit_message = input("请输入提交信息 (默认: Initial commit): ").strip()
        if not commit_message:
            commit_message = "Initial commit"
        
        if not self.commit_files(commit_message):
            return
        
        # 7. 获取GitHub Token
        token = self.get_github_token()
        if not token:
            return
        
        # 8. 添加远程仓库
        if not self.add_remote():
            return
        
        # 9. 推送到GitHub
        if not self.push_to_github():
            return
        
        print(f"\n=== 上传完成 ===")
        print(f"✓ 项目已成功上传到GitHub")
        print(f"✓ 仓库地址: {self.repo_url}")
        print(f"✓ 请访问上述地址查看您的项目")
        print("\n感谢使用破万法工具！")

def main():
    uploader = PowanfaUploader()
    uploader.run()

if __name__ == "__main__":
    main() 