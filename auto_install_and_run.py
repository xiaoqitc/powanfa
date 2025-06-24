#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
破万法工具箱 - 自动安装环境并启动
作者：小白
功能：自动安装所有依赖并启动工具箱
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class AutoInstaller:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.requirements_file = "requirements.txt"
        
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
    
    def check_python_version(self):
        """检查Python版本"""
        print("=== 检查Python环境 ===")
        success, stdout, stderr = self.run_command("python --version")
        if success:
            version = stdout.strip()
            print(f"✓ Python版本: {version}")
            
            # 检查版本号
            try:
                version_num = version.split()[1]
                major, minor = map(int, version_num.split('.')[:2])
                if major >= 3 and minor >= 7:
                    print("✓ Python版本符合要求 (3.7+)")
                    return True
                else:
                    print(f"✗ Python版本过低，需要3.7+，当前版本: {version_num}")
                    return False
            except:
                print("⚠️  无法解析Python版本，继续执行...")
                return True
        else:
            print("✗ Python未安装或无法运行")
            return False
    
    def check_pip(self):
        """检查pip是否可用"""
        print("\n=== 检查pip ===")
        success, stdout, stderr = self.run_command("pip --version")
        if success:
            print(f"✓ pip可用: {stdout.strip()}")
            return True
        else:
            print("✗ pip不可用")
            return False
    
    def upgrade_pip(self):
        """升级pip"""
        print("\n=== 升级pip ===")
        success, stdout, stderr = self.run_command("python -m pip install --upgrade pip")
        if success:
            print("✓ pip升级成功")
        else:
            print("⚠️  pip升级失败，继续执行...")
    
    def install_requirements(self):
        """安装依赖包"""
        print("\n=== 安装依赖包 ===")
        
        if not (self.current_dir / self.requirements_file).exists():
            print(f"✗ 找不到 {self.requirements_file} 文件")
            return False
        
        # 读取requirements.txt
        with open(self.requirements_file, 'r', encoding='utf-8') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"需要安装 {len(requirements)} 个依赖包:")
        for req in requirements:
            print(f"  - {req}")
        
        # 安装所有依赖
        success, stdout, stderr = self.run_command(f"pip install -r {self.requirements_file}")
        if success:
            print("✓ 所有依赖包安装成功")
            return True
        else:
            print(f"✗ 依赖包安装失败: {stderr}")
            return False
    
    def check_dependencies(self):
        """检查关键依赖是否安装成功"""
        print("\n=== 检查依赖安装 ===")
        
        critical_deps = ['PyQt5', 'flask', 'requests', 'PyJWT']
        all_installed = True
        
        for dep in critical_deps:
            try:
                if dep == 'PyQt5':
                    import PyQt5
                elif dep == 'flask':
                    import flask
                elif dep == 'requests':
                    import requests
                elif dep == 'PyJWT':
                    import jwt
                print(f"✓ {dep} 已安装")
            except ImportError:
                print(f"✗ {dep} 未安装")
                all_installed = False
        
        return all_installed
    
    def start_toolbox(self):
        """启动工具箱"""
        print("\n=== 启动破万法工具箱 ===")
        
        # 检查主程序文件是否存在
        main_program = "hacker_toolbox.py"
        if not (self.current_dir / main_program).exists():
            print(f"✗ 找不到主程序文件: {main_program}")
            return False
        
        print("正在启动工具箱...")
        print("请稍等，程序正在加载...")
        
        # 启动主程序
        try:
            # 使用subprocess.Popen启动程序，不等待其结束
            process = subprocess.Popen([sys.executable, main_program], 
                                     cwd=self.current_dir,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            
            print("✓ 工具箱启动成功！")
            print("程序已在后台运行，请查看新打开的窗口")
            
            # 等待一下确保程序启动
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"✗ 启动工具箱失败: {e}")
            return False
    
    def run(self):
        """运行完整的安装和启动流程"""
        print("=== 破万法工具箱 - 自动安装环境 ===")
        print("作者：小白  微信：ccyuwu8888  QQ：154418587")
        print()
        
        # 1. 检查Python版本
        if not self.check_python_version():
            print("\n请先安装Python 3.7+")
            print("下载地址: https://www.python.org/downloads/")
            input("按回车键退出...")
            return
        
        # 2. 检查pip
        if not self.check_pip():
            print("\n请先安装pip")
            input("按回车键退出...")
            return
        
        # 3. 升级pip
        self.upgrade_pip()
        
        # 4. 安装依赖
        if not self.install_requirements():
            print("\n依赖安装失败，请检查网络连接")
            input("按回车键退出...")
            return
        
        # 5. 检查依赖
        if not self.check_dependencies():
            print("\n部分依赖安装失败，请手动安装")
            input("按回车键退出...")
            return
        
        # 6. 启动工具箱
        if self.start_toolbox():
            print("\n=== 安装和启动完成 ===")
            print("✓ 环境安装成功")
            print("✓ 工具箱已启动")
            print("\n感谢使用破万法工具！")
        else:
            print("\n✗ 启动失败")
        
        input("\n按回车键退出...")

def main():
    installer = AutoInstaller()
    installer.run()

if __name__ == "__main__":
    main() 