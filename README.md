# 破万法 - 黑客工具箱

<div align="center">

![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.7+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Author](https://img.shields.io/badge/Author-小白-orange.svg)

**一个功能强大的加密解码分析工具，支持多种编码格式的自动识别和暴力破解**

[![GitHub stars](https://img.shields.io/github/stars/xiaoqitc/powanfa.svg?style=social&label=Star)](https://github.com/xiaoqitc/powanfa)
[![GitHub forks](https://img.shields.io/github/forks/xiaoqitc/powanfa.svg?style=social&label=Fork)](https://github.com/xiaoqitc/powanfa)

</div>

---

## 🚀 功能特性

- 🔐 **多格式解码**: 支持Base64、Base32、Base16、URL编码、Hex、JWT、HTML实体、ROT13、Unicode转义等
- 🔍 **智能识别**: 自动识别MD5、SHA1、SHA256等哈希值
- 💥 **暴力破解**: 内置弱口令字典和在线API爆破功能
- 📊 **可视化大屏**: 实时数据统计和图表展示
- 🌐 **多语言支持**: 中文、英文、日文界面
- 🎨 **现代化UI**: 基于PyQt5的炫酷黑客风格界面
- 🔧 **一键部署**: 支持GitHub自动上传和项目打包

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

## 🎯 使用方法

### 图形界面版本
```bash
python hacker_toolbox.py
```

### Web版本
```bash
python web_app.py
```

### 命令行版本
```bash
python core_decoder.py
```

### 一键启动（推荐）
```bash
# Windows用户直接双击
start_all.bat
```

## 🔧 功能模块

### 1. 加密解码分析
- **自动识别**: 智能识别多种编码格式
- **递归解码**: 支持嵌套编码的递归解码
- **实时显示**: 实时显示解码路径和结果
- **批量处理**: 支持批量内容分析

### 2. 可视化大屏
- **ECharts图表**: 基于ECharts的数据可视化
- **实时统计**: 实时统计解码成功率
- **多图表类型**: 支持柱状图、饼图等多种图表
- **响应式设计**: 自适应不同屏幕尺寸

### 3. 爆破工具
- **多算法支持**: MD5、AES、DES、RC4等
- **内置字典**: Top1000弱口令字典
- **自定义字典**: 支持用户上传自定义字典
- **在线API**: 集成多个在线破解API服务
- **进度显示**: 实时显示爆破进度

## 📋 支持的编码格式

| 格式 | 描述 | 示例 | 状态 |
|------|------|------|------|
| Base64 | Base64编码 | `SGVsbG8gV29ybGQ=` | ✅ |
| Base32 | Base32编码 | `JBSWY3DPEBLW64TMMQ======` | ✅ |
| Base16 | Base16编码 | `48656C6C6F20576F726C64` | ✅ |
| URL编码 | URL编码 | `Hello%20World` | ✅ |
| Hex | 十六进制 | `48656C6C6F20576F726C64` | ✅ |
| JWT | JSON Web Token | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | ✅ |
| HTML实体 | HTML实体编码 | `&lt;Hello World&gt;` | ✅ |
| ROT13 | ROT13编码 | `Uryyb Jbeyq` | ✅ |
| Unicode转义 | Unicode转义序列 | `\\u0048\\u0065\\u006C\\u006C\\u006F` | ✅ |

## 🔍 哈希识别

自动识别以下哈希类型：
- **MD5** (32位十六进制) - `5d41402abc4b2a76b9719d911017c592`
- **SHA1** (40位十六进制) - `aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d`
- **SHA256** (64位十六进制) - `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824`

## 💥 爆破功能

### 内置弱口令
包含常见的弱口令如：
- `123456`, `password`, `admin`, `qwerty`
- `letmein`, `111111`, `abc123`, `123123`
- `12345678`, `123456789`, `root`, `user`
- `test`, `pass`, `000000`, `654321`

### 在线API
集成多个在线破解API：
- **toolshu.com API** - 专业哈希破解服务
- **nmd5.com API** - MD5在线破解
- **自定义API** - 支持用户自定义API接口

## 📁 项目结构

```
powanfa/
├── hacker_toolbox.py      # 主程序（图形界面）
├── core_decoder.py        # 核心解码模块
├── web_app.py            # Web版本
├── requirements.txt      # 依赖包列表
├── start_all.bat        # 启动脚本
├── github_upload.py     # GitHub上传脚本
├── upload_to_github.bat # 快速上传脚本
├── test_github_upload.py # 测试脚本
├── test_github.bat      # 测试启动脚本
├── package_project.py   # 项目打包脚本
├── package_project.bat  # 打包启动脚本
├── GitHub上传说明.md    # 上传说明文档
└── README.md           # 项目说明文档
```

## 🛠️ 开发环境

- **Python**: 3.7+
- **GUI框架**: PyQt5
- **Web框架**: Flask
- **图表库**: ECharts
- **HTTP库**: requests
- **JWT库**: PyJWT

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/xiaoqitc/powanfa.git
cd powanfa
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行程序
```bash
# 图形界面版本
python hacker_toolbox.py

# 或使用一键启动
start_all.bat
```

### 4. 上传到GitHub
```bash
# 使用上传脚本
python github_upload.py

# 或使用批处理脚本
upload_to_github.bat
```

## 📸 界面预览

### 主界面
- 炫酷的黑客风格界面
- 多语言支持（中文/英文/日文）
- 响应式布局设计

### 解码分析
- 实时解码结果显示
- 多种编码格式支持
- 智能识别和提示

### 可视化大屏
- 实时数据统计图表
- 交互式图表展示
- 美观的数据可视化

## 🔧 配置说明

### 环境变量
```bash
# 设置Python路径（如果需要）
export PYTHONPATH=/path/to/python

# 设置代理（如果需要）
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

### 配置文件
项目支持自定义配置：
- API接口地址
- 字典文件路径
- 界面语言设置
- 主题样式配置

## 🐛 常见问题

### Q: 程序无法启动
**A:** 
1. 检查Python版本是否为3.7+
2. 确认已安装所有依赖：`pip install -r requirements.txt`
3. 检查PyQt5是否正确安装

### Q: 解码失败
**A:**
1. 确认输入内容格式正确
2. 检查网络连接（在线API需要）
3. 尝试不同的解码方式

### Q: GitHub上传失败
**A:**
1. 检查Git是否已安装
2. 确认GitHub Token有效
3. 检查网络连接
4. 查看详细错误信息

### Q: 界面显示异常
**A:**
1. 检查PyQt5版本兼容性
2. 尝试重新安装PyQt5
3. 检查系统字体支持

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 提交Issue
1. 使用Issue模板
2. 详细描述问题
3. 提供复现步骤
4. 附上错误日志

### 提交PR
1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

**注意**: 本项目仅供学习和研究使用，请勿用于非法用途。

## 👨‍💻 作者信息

- **作者**: 小白
- **微信**: ccyuwu8888
- **QQ**: 154418587
- **GitHub**: [@xiaoqitc](https://github.com/xiaoqitc)

## 🙏 致谢

感谢以下开源项目的支持：
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI框架
- [Flask](https://flask.palletsprojects.com/) - Web框架
- [ECharts](https://echarts.apache.org/) - 图表库
- [requests](https://requests.readthedocs.io/) - HTTP库

## 📈 更新日志

### v1.0.0 (2024-12-19)
- ✨ 初始版本发布
- 🔐 支持多种编码格式解码
- 🎨 集成图形界面和Web界面
- 💥 添加爆破工具功能
- 📊 实现可视化大屏
- 🌐 支持多语言界面
- 🔧 添加GitHub上传工具
- 📦 支持项目打包功能

---

<div align="center">

⭐ **如果这个项目对你有帮助，请给个Star支持一下！** ⭐

[![GitHub stars](https://img.shields.io/github/stars/xiaoqitc/powanfa.svg?style=social&label=Star)](https://github.com/xiaoqitc/powanfa)
[![GitHub forks](https://img.shields.io/github/forks/xiaoqitc/powanfa.svg?style=social&label=Fork)](https://github.com/xiaoqitc/powanfa)

</div> 