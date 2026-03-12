# OpenClaw StepFun Search Skill

实时网络搜索工具，基于 StepFun API。支持学术、编程、商业、政府等多分类搜索。

## 🚀 快速开始

> 这里的安装是给openclaw看的，实际用户只需要将这个项目链接发给openclaw，就可以自动安装

### 1. 安装

```bash
# 复制到你的 OpenClaw skills 目录
cp -r stepfun-search ~/.openclaw/workspace/skills/
```

### 2. 配置 API Key

编辑 `~/.openclaw/openclaw.json`，添加以下配置：

```json
{
  "skills": {
    "entries": {
      "stepfun-search": {
        "enabled": true,
        "env": {
          "STEPFUN_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

**获取 API Key：**
1. 访问 [StepFun 官网](https://platform.stepfun.com/docs/zh/api-reference/Search/search)
2. 注册账号并登录
3. 在控制台中申请 API Key
4. 复制 Key 到上面的配置中

### 3. 使用

在 OpenClaw 中直接说：
- **"联网搜索 transformer attention mechanism"** → 学术搜索
- **"网络搜索 Python asyncio tutorial"** → 编程搜索  
- **"搜索 AI startup funding" (business)** → 商业搜索

或用 CLI：

```bash
python3 scripts/stepfun_search.py "your query" 5 research json
```

## 📖 详细文档

- **[SKILL.md](./SKILL.md)** - 完整功能说明、搜索类别、最佳实践
- **[API Reference](./references/api-reference.md)** - API 文档

## 🔍 搜索类别

| 类别 | 用途 | 例子 |
|------|------|------|
| `research` | 学术论文、研究报告、技术文档 | "Transformer 论文" |
| `programming` | 代码示例、技术教程、API 参考 | "Python asyncio" |
| `business` | 商业新闻、市场分析、公司信息 | "AI startup funding" |
| `gov` | 政府文件、政策法规、官方信息 | "数据隐私法规" |

## 💡 搜索技巧

✅ **好的查询：**
- 具体明确：`"Stable Diffusion fine-tuning"`
- 领域特定：使用分类参数
- 关键词组合：`"PyTorch image classification"`

❌ **避免：**
- 过于宽泛：`"Image"`, `"Data"`
- 完整句子：用关键词替代
- 过长查询：>200 字符

## ⚙️ 输出格式

支持三种输出格式：
- **JSON** - 结构化数据（默认）
- **Markdown** - 文档格式
- **Text** - 纯文本

## 📊 限流

- 请求超时：30 秒
- 最大结果：10 个
- 缓存 TTL：15 分钟

## 🐛 故障排查

| 问题 | 解决方案 |
|------|--------|
| `STEPFUN_API_KEY not set` | 检查 `~/.openclaw/openclaw.json` 配置 |
| `Authorization failed` | 验证 API Key 有效性 |
| `Timeout` | 简化查询或重试 |
| `No results found` | 尝试不同关键词或更改类别 |

## 📝 文件结构

```
stepfun-search/
├── SKILL.md                    # OpenClaw skill 定义
├── README.md                   # 本文件
├── scripts/
│   └── stepfun_search.py      # 搜索脚本
└── references/
    └── api-reference.md        # API 完整文档
```

## 🔒 安全提示

⚠️ **永远不要：**
- 将 API Key 提交到 Git
- 在代码中硬编码 Key
- 分享 openclaw.json 文件

✅ **应该：**
- 将 API Key 存储在 `~/.openclaw/openclaw.json`
- 使用环境变量管理敏感信息
- 定期更新和轮换 API Key

## 📄 License

MIT

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Created with ❤️ by OpenClaw Community**
