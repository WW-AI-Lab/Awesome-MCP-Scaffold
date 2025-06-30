# 🚀 Awesome-MCP-Scaffold

> **生产级 MCP 服务器开发脚手架 - 专为 Cursor IDE 优化的快速开发解决方案**

[English](README_EN.md) | 中文

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-v1.10.1-green.svg)](https://modelcontextprotocol.io)
[![Streamable HTTP](https://img.shields.io/badge/Transport-Streamable%20HTTP-orange.svg)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Production%20Ready-blue.svg)](docs/DOCKER_OPTIMIZATION.md)

## 🎯 项目定位

**Awesome-MCP-Scaffold** 是一个**开箱即用的 MCP 服务器开发脚手架**，让你能够：

- 🚀 **5分钟启动**：从零到运行的完整 MCP 服务器
- 🤖 **10分钟MCP开发**：内置提示词和范例，基于 Cursor IDE 一句话完成MCP Server tools开发
- 🏭 **生产级架构**：经过验证的高性能部署方案
- 📚 **最佳实践内置**：遵循官方 MCP SDK v1.10.1 规范

## ✨ 核心优势

### 🔥 专为 Cursor 优化
- **智能规则系统**：内置用户Rules [Cursor_User_Rules.md](docs/Cursor_User_Rules.md)和 3 套项目 `.cursor/rules` 配置
- **AI 代码生成**：一句话自动生成 Tools、Resources、Prompts，并自动生成测试用例
- **上下文感知**：AI 助手理解 MCP 开发模式
- **错误自动修复**：智能识别并修复常见问题

### ⚡ 开箱即用的完整功能
- **12+ 示例工具**：计算器、文本处理、文件操作等
- **多种资源类型**：系统信息、配置数据等
- **提示模板**：代码审查、数据分析等场景
- **REST API 端点**：支持外挂完整的 HTTP API 支持，便于与不支持MCP的平台对接

### 🏗️ 生产级架构
- **Streamable HTTP 优先**：最新传输协议，3-5倍性能提升
- **Docker 优化**：多进程部署，智能资源管理
- **负载均衡**：Nginx 配置，支持水平扩展
- **监控集成**：Prometheus + Grafana 开箱即用

## 🚀 5分钟快速开始

### 1. 克隆脚手架

```bash
# 使用脚手架创建新项目
git clone https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold.git my-mcp-server
cd my-mcp-server

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动开发服务器

```bash
# 开发模式 (stdio)
python run.py

# HTTP 模式 (推荐)
python run.py --transport streamable-http --port 8000

# 使用 FastMCP CLI
fastmcp dev run.py
```

### 3. 验证MCP服务器

```bash
# MCP协议测试 - 获取工具列表
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python run.py

# MCP协议测试 - 获取资源列表  
echo '{"jsonrpc":"2.0","id":2,"method":"resources/list"}' | python run.py

# MCP协议测试 - 调用计算器工具
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"calculator","arguments":{"expression":"2+3*4"}}}' | python run.py

# HTTP模式下的MCP端点测试
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### 4. 在 Cursor 中开发

1. **打开项目**：在 Cursor 中打开项目文件夹
2. **AI 助手激活**：Cursor 自动加载 `.cursor/rules` 配置
3. **开始开发**：按 `Cmd/Ctrl+K` 输入需求，AI 自动生成代码

## 📁 脚手架结构

```
awesome-mcp-scaffold/
├── 🎯 核心架构
│   ├── server/                 # MCP 服务器核心
│   │   ├── main.py            # FastMCP 主实例
│   │   ├── config.py          # 配置管理
│   │   ├── tools/             # 工具实现 (12+ 示例)
│   │   ├── resources/         # 资源实现
│   │   ├── prompts/           # 提示模板
│   │   └── routes/            # REST API 路由
│   └── run.py                 # 启动入口
│
├── 🤖 Cursor 集成
│   └── .cursor/rules/         # AI 规则配置
│       ├── mcp-development-guide.mdc
│       ├── streamable-http-production.mdc
│       └── mcp-testing-patterns.mdc
│
├── 🏭 生产部署
│   ├── Dockerfile             # 生产级容器配置
│   ├── docker-compose.yml     # 多环境部署
│   ├── docker-entrypoint.sh   # 智能启动脚本
│   └── deploy/                # 部署配置
│       ├── nginx/             # 负载均衡
│       └── kubernetes/        # K8s 配置
│
├── 📚 文档指南
│   ├── docs/GETTING_STARTED.md
│   ├── docs/CURSOR_GUIDE.md
│   ├── docs/DOCKER_OPTIMIZATION.md
│   └── docs/BEST_PRACTICES.md
│
└── 🧪 测试验证
    ├── tests/                 # 完整测试套件
    ├── Makefile              # 开发命令
    └── pyproject.toml        # 项目配置
```

## 🤖 Cursor AI 开发体验

### 智能代码生成

**创建新工具** - 在 Cursor 中按 `Cmd/Ctrl+K`：
```
"创建一个天气查询工具，支持城市名和坐标查询，一步一步努力完成目标"
```

AI 自动生成：
```python
@mcp.tool(title="Weather Query", description="Query weather by city or coordinates")
def get_weather(location: str, units: str = "metric") -> Dict[str, Any]:
    """Query current weather information."""
    # 完整的实现代码...
```

**添加资源** - 继续对话：
```
"为天气工具添加一个配置资源，支持 API 密钥管理"
```

**生成测试** - 一键生成：
```
"为天气工具生成完整的测试用例"
```

### 三套专业规则

| 规则文件 | 用途 | 触发场景 |
|---------|------|----------|
| `mcp-development-guide.mdc` | MCP 开发指导 | 开发 Tools/Resources/Prompts |
| `streamable-http-production.mdc` | 生产部署优化 | 部署配置和性能优化 |
| `mcp-testing-patterns.mdc` | 测试最佳实践 | 编写和优化测试代码 |

## 🏭 生产级部署

### Docker 一键部署

```bash
# 构建生产镜像
docker build -t my-mcp-server .

# 启动生产服务器 (自动多进程)
docker run -d \
  --name mcp-server \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  my-mcp-server
```

### Docker Compose 完整栈

```bash
# 启动完整服务栈
docker-compose up -d
```

## 📊 内置示例功能

### 🛠️ Tools (工具)
- **计算器**：基础数学运算、BMI计算、百分比计算
- **文本处理**：单词统计、格式转换、正则提取
- **文件操作**：安全的文件读写、JSON处理

### 📡 Resources (资源)
- **系统信息**：CPU、内存、磁盘状态监控
- **配置数据**：应用配置、版本信息管理

### 💬 Prompts (提示)
- **代码审查**：质量分析、Bug检测、性能优化
- **数据分析**：统计分析、预测建模、质量评估

### 🌐 MCP协议端点
- **主要端点**: `/mcp` - MCP协议通信端点
- **传输协议**: Streamable HTTP (推荐) / stdio
- **协议格式**: JSON-RPC 2.0

### 🔧 可选REST API (便于第三方集成)
- `/health` - 健康检查
- `/info` - 服务器信息  
- `/api/tools` - 工具列表 (非MCP协议)

## 🧪 验证和测试

### 自动化测试套件
```bash
# 运行完整测试
make test

# 代码质量检查
make lint

# 测试覆盖率
make coverage
```

### MCP协议验证步骤
```bash
# 1. MCP核心功能测试
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python run.py
echo '{"jsonrpc":"2.0","id":2,"method":"resources/list"}' | python run.py

# 2. MCP工具调用测试
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"calculator","arguments":{"expression":"10*5+2"}}}' | python run.py

# 3. HTTP模式MCP测试
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# 4. 可选的健康检查 (非MCP协议)
curl http://localhost:8000/health
```

## 📚 学习资源

### 新手指南
- 📖 [5分钟快速开始](docs/GETTING_STARTED.md)
- 🎯 [Cursor 使用指南](docs/CURSOR_GUIDE.md)
- 🏗️ [最佳实践](docs/BEST_PRACTICES.md)

### 进阶指南
- 🐳 [Docker 生产优化](docs/DOCKER_OPTIMIZATION.md)
- 🚀 [性能调优指南](docs/PERFORMANCE_TUNING.md)
- 📊 [监控和运维](docs/MONITORING.md)

### 官方资源
- 🌐 [MCP 官方文档](https://modelcontextprotocol.io)
- 📦 [Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 🎉 成功案例

基于此脚手架构建的生产项目：

- **[any2markdown](https://github.com/WW-AI-Lab/any2markdown)** - 一个高性能的文档转换服务器，同时支持 Model Context Protocol (MCP) 和 RESTful API 接口。将 PDF、Word 和 Excel 文档转换为 Markdown 格式，具备图片提取、页眉页脚移除和批量处理等高级功能
- **[azure-gpt-image](https://github.com/WW-AI-Lab/azure-gpt-image)** - 一个基于Azure OpenAI gpt-image-1模型的Model Context Protocol (MCP) 服务器，使用官方MCP SDK的Streamable HTTP Transport实现，为AI助手提供强大的图像生成和编辑能力
- **[jinja2-mcp-server](https://github.com/WW-AI-Lab/jinja2-mcp-server)** - 一个基于Jinja2模板的Model Context Protocol (MCP) 服务器，使用官方MCP SDK的Streamable HTTP Transport实现，为AI助手提供强大的模板渲染能力

## 🤝 社区支持

### 获取帮助
- 💬 [GitHub Discussions](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/discussions)
- 🐛 [问题反馈](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/issues)
- 📧 **邮箱**: toxingwang@gmail.com

### 贡献指南
- 🔄 [贡献流程](CONTRIBUTING.md)
- 📋 [开发规范](docs/DEVELOPMENT.md)
- 🧪 [测试指南](docs/TESTING.md)

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) - 可自由用于商业和开源项目。

## 🙏 致谢

感谢以下项目和社区的支持：

- **[Anthropic](https://anthropic.com)** - MCP 协议的创建者
- **[Cursor](https://cursor.sh)** - AI 驱动的代码编辑器
- **[WW-AI-Lab](https://github.com/WW-AI-Lab)** - AI 实验室社区

---

**🚀 立即开始你的 MCP 服务器开发之旅！**

如果这个脚手架对你有帮助，请给我们一个 ⭐️ 