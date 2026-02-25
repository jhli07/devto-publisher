# 🚀 Dev.to 自动发布系统

用 Python 一键发布技术文章到 Dev.to 开发者社区。

## ✨ 特性

- 📝 **一键发布** - 简单命令发布文章
- 🤖 **内容生成** - 内置多篇预设文章
- 🏷️ **自动标签** - 自动添加相关标签
- 🔐 **安全认证** - API Key 环境变量管理

## 📦 安装

```bash
git clone https://github.com/jhli07/devto-publisher.git
cd devto-publisher
pip install requests
```

## 🔧 配置

### 获取 API Key

1. 登录 [Dev.to](https://dev.to)
2. 进入 [Settings → Account](https://dev.to/settings/account)
3. 找到 **API Keys** 部分
4. 点击 **Generate new API key**
5. 复制生成的 Key

### 设置环境变量

```bash
# Linux/Mac
export DEVTO_API_KEY="你的-api-key"

# Windows
set DEVTO_API_KEY=你的-api-key

# 永久保存 (Mac/Linux)
echo 'export DEVTO_API_KEY="你的-api-key"' >> ~/.zshrc
source ~/.zshrc
```

## 🚀 使用

### 基本使用

```bash
python devto_publisher.py
```

系统会：
1. 自动选择一篇预设文章
2. 发布到你的 Dev.to 账户
3. 显示文章链接

### Python API

```python
from devto_publisher import DevToPublisher, ContentGenerator

# 初始化
publisher = DevToPublisher(api_key="your-api-key")

# 发布文章
result = publisher.publish_article(
    title="我的第一篇文章",
    content="# Hello World\n\n这是一篇测试文章。",
    tags=["python", "tutorial"],
    published=True
)

if result["status"] == "success":
    print(f"发布成功: {result['url']}")
```

### 发布自定义文章

```python
from devto_publisher import DevToPublisher

publisher = DevToPublisher()

# 从文件读取
with open("my_article.md", "r") as f:
    content = f.read()

result = publisher.publish_article(
    title="自定义文章标题",
    content=content,
    tags=["automation", "python"]
)
```

## 📝 预设话题

| # | 标题 | 标签 |
|---|------|------|
| 1 | 为什么你应该现在开始学习 AI 自动化？ | ai, automation, productivity |
| 2 | Python 自动化脚本实战 | python, automation, tutorial |
| 3 | GitHub Actions 实战 | github, cicd, devops |

## 🔒 安全提示

- **不要** 将 API Key 上传到 GitHub
- 使用 **环境变量** 而非硬编码
- 定期 **轮换** API Key

## 📊 变现思路

1. **Dev.to Partner Program** - 获取广告收入
2. **联盟营销** - 在文章中插入链接
3. **引流** - 将读者引导到你的产品/服务

## 📄 许可证

MIT License

---

*Built with ❤️ by Agent_Li*
