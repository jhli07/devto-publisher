#!/usr/bin/env python3
"""
Dev.to 自动发布系统
Dev.to Automated Publishing System

支持功能：
- 一键发布文章到 Dev.to
- Markdown 格式自动转换
- 自动标签生成
- 定时发布（可选）
"""

import os
import sys
import json
import time
import datetime
from typing import Optional, Dict, List
import requests

# 配置
API_BASE = "https://dev.to/api"


class DevToPublisher:
    """Dev.to 发布器"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEVTO_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
    
    def get_user(self) -> Dict:
        """获取当前用户信息"""
        if not self.api_key:
            return {"error": "No API key provided"}
        
        response = requests.get(f"{API_BASE}/me", headers=self.headers)
        return response.json()
    
    def publish_article(
        self,
        title: str,
        content: str,
        tags: List[str] = None,
        published: bool = True,
        canonical_url: str = None,
        description: str = None
    ) -> Dict:
        """
        发布文章到 Dev.to
        
        Args:
            title: 文章标题
            content: Markdown 内容
            tags: 标签列表（最多4个）
            published: 是否立即发布
            canonical_url: 原文链接（用于聚合文章）
            description: 文章描述（SEO）
        """
        if not self.api_key:
            return {"error": "请设置 DEVTO_API_KEY 环境变量"}
        
        # 限制标签数量
        if tags and len(tags) > 4:
            tags = tags[:4]
        
        data = {
            "article": {
                "title": title,
                "body_markdown": content,
                "published": published,
                "tags": tags or ["python", "automation", "ai"],
            }
        }
        
        # 添加可选字段
        if description:
            data["article"]["description"] = description
        if canonical_url:
            data["article"]["canonical_url"] = canonical_url
        
        try:
            response = requests.post(
                f"{API_BASE}/articles",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 201:
                article = response.json()["article"]
                return {
                    "status": "success",
                    "url": article["url"],
                    "id": article["id"],
                    "title": article["title"]
                }
            else:
                return {
                    "status": "error",
                    "code": response.status_code,
                    "message": response.text
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_article(self, article_id: int, **kwargs) -> Dict:
        """更新已发布的文章"""
        if not self.api_key:
            return {"error": "No API key provided"}
        
        data = {"article": kwargs}
        
        try:
            response = requests.put(
                f"{API_BASE}/articles/{article_id}",
                headers=self.headers,
                json=data
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_articles(self, username: str = None) -> List[Dict]:
        """获取文章列表"""
        if username:
            response = requests.get(f"{API_BASE}/articles?username={username}")
        else:
            response = requests.get(f"{API_BASE}/articles/me", headers=self.headers)
        
        return response.json()


class ContentGenerator:
    """内容生成器 - 用于生成适合 Dev.to 的文章"""
    
    # 预置话题库
    TOPICS = [
        {
            "title": "为什么你应该现在开始学习 AI 自动化？",
            "tags": ["ai", "automation", "productivity"],
            "content": """
# 为什么你应该现在开始学习 AI 自动化？

在人工智能飞速发展的今天，你是否感到焦虑和迷茫？

每天都有新的 AI 工具问世，与其被动焦虑，不如主动拥抱变化。

## 什么是 AI 自动化？

AI 自动化不仅仅是使用 ChatGPT 写代码，它是一套系统化的方法：

1. **任务分析** - 识别哪些工作可以被 AI 替代或增强
2. **流程设计** - 构建人机协作的工作流程
3. **工具链集成** - 将多个 AI 工具串联成自动化流水线
4. **持续优化** - 根据反馈不断调整和改进

## 我的 AI 自动化实践

### 代码审查自动化

```python
import openai

def review_code(code: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一个资深代码审查专家"},
            {"role": "user", "content": f"请审查以下代码并给出建议:\n\n{code}"}
        ]
    )
    return response.choices[0].message.content
```

### 技术文档写作

写技术文档是很多开发者的噩梦，现在 30 分钟完成以前一天的工作。

### 数据分析报告

面对海量数据，AI 帮助自动发现异常和趋势。

## AI 自动化的核心优势

- **效率提升 10 倍以上**
- **质量更稳定**
- **学习曲线更平缓**

## 如何开始？

1. **选择你的工具** - ChatGPT、Claude、GitHub Copilot
2. **从一个小项目开始**
3. **建立自己的提示词库**
4. **持续迭代**

## 结语

现在是开始学习 AI 自动化的最佳时机。不是因为它会让你的工作消失，而是因为它会让你的工作更有价值。

---

*本文由 AI 辅助创作*
            """
        },
        {
            "title": "Python 自动化脚本实战：从入门到精通",
            "tags": ["python", "automation", "tutorial"],
            "content": """
# Python 自动化脚本实战

Python 是自动化领域的瑞士军刀。本文分享 5 个实用的自动化脚本。

## 1. 文件自动整理脚本

```python
import os
import shutil
from pathlib import Path

def organize_downloads(download_dir: str):
    """自动整理下载文件夹"""
    patterns = {
        "Images": [".png", ".jpg", ".gif", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt"],
        "Archives": [".zip", ".rar", ".7z"],
        "Videos": [".mp4", ".mkv", ".avi"]
    }
    
    for file in Path(download_dir).iterdir():
        if file.is_file():
            for folder, exts in patterns.items():
                if file.suffix.lower() in exts:
                    target = Path(download_dir) / folder
                    target.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target / file.name))
                    print(f"Moved {file.name} to {folder}/")
```

## 2. 网页内容监控

```python
import requests
from bs4 import BeautifulSoup

def monitor_price(url: str, target_price: float):
    """监控商品价格"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 提取价格（根据网站结构调整）
    price = float(soup.select_one(".price").text.strip("$"))
    
    if price <= target_price:
        print(f"价格已降至 ${price}！")
    else:
        print(f"当前价格 ${price}，目标 ${target_price}")
```

## 3. Excel 数据处理

```python
import pandas as pd

def process_excel(input_file: str, output_file: str):
    """自动化 Excel 处理"""
    df = pd.read_excel(input_file)
    
    # 数据清洗
    df.dropna(inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    
    # 数据统计
    summary = df.groupby("category")["amount"].sum()
    
    # 输出
    summary.to_excel(output_file)
    print(f"处理完成，结果已保存到 {output_file}")
```

## 4. 定时任务调度

```python
import schedule
import time

def job():
    print("执行定时任务...")

# 设置定时任务
schedule.every().day.at("09:00").do(job)
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 5. 邮件自动发送

```python
import smtplib
from email.mime.text import MIMEText

def send_email(to: str, subject: str, body: str):
    """发送邮件"""
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "your@email.com"
    msg["To"] = to
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your@email.com", "password")
        server.send_message(msg)
```

## 总结

自动化不是让工作消失，而是让我们专注于更有价值的事情。

---

*本文由 AI 辅助创作*
            """
        },
        {
            "title": "GitHub Actions 实战：打造你的 CI/CD 自动化流水线",
            "tags": ["github", "cicd", "devops"],
            "content": """
# GitHub Actions 实战

GitHub Actions 是 GitHub 自带的 CI/CD 工具，完全免费！

## 什么是 CI/CD？

- **CI (Continuous Integration)** - 持续集成
- **CD (Continuous Deployment)** - 持续部署

简单说：代码提交 → 自动测试 → 自动部署

## 第一个 Workflow

创建 `.github/workflows/ci.yml`：

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
```

## 自动化部署到服务器

```yaml
deploy:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Server
        uses: appleboy/ssh-action@v0.1.3
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_KEY }}
          script: |
            cd /path/to/project
            git pull
            docker-compose up -d
```

## 自动发布 Release

```yaml
release:
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref_name }}
          release_name: Release ${{ github.ref_name }}
          draft: false
          prerelease: false
```

## 常用 Actions

| Action | 用法 |
|--------|------|
| actions/checkout | 检出代码 |
| actions/setup-python | 设置 Python |
| appleboy/ssh-action | SSH 连接 |
|.codecov/codecov-action | 代码覆盖率 |

## 最佳实践

1. **使用缓存** - 加速构建
2. **矩阵策略** - 多版本测试
3. **手动审批** - 生产环境部署需要确认
4. **Secrets 管理** - 敏感信息放 Secrets

---

*本文由 AI 辅助创作*
            """
        }
    ]
    
    def get_topic(self, index: int = None) -> Dict:
        """获取预设话题"""
        if index is None:
            import random
            index = random.randint(0, len(self.TOPICS) - 1)
        return self.TOPICS[index]
    
    def list_topics(self) -> List[str]:
        """列出所有话题"""
        return [t["title"] for t in self.TOPICS]


def main():
    """主函数"""
    print("=" * 50)
    print("🚀 Dev.to 自动发布系统")
    print("=" * 50)
    
    # 检查 API Key
    api_key = os.getenv("DEVTO_API_KEY")
    if not api_key:
        print("\n❌ 未设置 DEVTO_API_KEY")
        print("请设置环境变量：")
        print("  export DEVTO_API_KEY='你的-dev.to-api-key'")
        print("\n获取方式：")
        print("  1. 访问 https://dev.to/settings/account")
        print("  2. 找到 'API Keys' 部分")
        print("  3. 创建新的 API Key")
        return
    
    publisher = DevToPublisher(api_key)
    
    # 获取用户信息
    user = publisher.get_user()
    if "error" in user:
        print(f"❌ API 错误: {user['error']}")
        return
    
    print(f"\n✅ 已连接：{user.get('name', user.get('username', 'User'))}")
    
    # 选择话题
    generator = ContentGenerator()
    print("\n📝 可用话题：")
    for i, title in enumerate(generator.list_topics(), 1):
        print(f"  {i}. {title}")
    
    choice = input("\n选择话题 (直接回车随机): ").strip()
    if choice:
        try:
            topic = generator.TOPICS[int(choice) - 1]
        except:
            topic = generator.get_topic()
    else:
        topic = generator.get_topic()
    
    # 发布
    print(f"\n📤 正在发布：{topic['title']}...")
    result = publisher.publish_article(
        title=topic["title"],
        content=topic["content"],
        tags=topic["tags"]
    )
    
    if result.get("status") == "success":
        print(f"\n✅ 发布成功！")
        print(f"🔗 文章链接: {result['url']}")
    else:
        print(f"\n❌ 发布失败: {result}")


if __name__ == "__main__":
    main()
