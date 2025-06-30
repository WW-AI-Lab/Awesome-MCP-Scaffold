# 📖 5分钟快速开始指南

> 从零开始，5分钟内启动你的第一个 MCP 服务器

## 🎯 开始之前

### 环境要求
- **Python 3.10+** (推荐 3.11+)
- **Cursor IDE** (强烈推荐，获得最佳 AI 开发体验)
- **Git** (用于克隆脚手架)

### 可选工具
- **Docker** (用于容器化部署)
- **uv** (更快的 Python 包管理器)

## 🚀 步骤 1：获取脚手架

```bash
# 克隆脚手架到本地
git clone https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold.git my-mcp-server
cd my-mcp-server

# 重命名为你的项目
# 可选：删除 .git 目录，重新初始化
rm -rf .git
git init
```

## 🔧 步骤 2：环境配置

### 方案 A：使用 pip (推荐新手)

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
```

### 方案 B：使用 uv (更快)

```bash
# 安装 uv (如果未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建项目并安装依赖
uv sync
```

## ⚡ 步骤 3：启动服务器

### 开发模式 (stdio)

```bash
# 最简单的启动方式
python run.py

# 使用 FastMCP CLI (推荐开发时使用)
fastmcp dev run.py
```

### HTTP 模式 (推荐)

```bash
# 启动 HTTP 服务器
python run.py --transport streamable-http --port 8000

# 后台运行
python run.py --transport streamable-http --port 8000 &
```

## ✅ 步骤 4：验证功能

### 基础健康检查

```bash
# 检查服务器状态
curl http://localhost:8000/health

# 预期输出:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "app_name": "Awesome MCP Server",
#   "environment": "development"
# }
```

### 查看服务器信息

```bash
# 获取详细信息
curl http://localhost:8000/info | python -m json.tool

# 预期输出:
# {
#   "name": "Awesome MCP Server",
#   "mcp_version": "1.10.1",
#   "capabilities": {
#     "tools": true,
#     "resources": true,
#     "prompts": true
#   }
# }
```

### 测试内置工具

```bash
# 查看可用工具
curl http://localhost:8000/api/tools

# 测试计算器工具
curl -X POST http://localhost:8000/api/tools/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5}'
```

## 🤖 步骤 5：Cursor AI 开发

### 1. 在 Cursor 中打开项目

```bash
# 在 Cursor 中打开
cursor .

# 或者手动打开 Cursor，然后打开项目文件夹
```

### 2. 验证 AI 规则加载

- Cursor 会自动识别 `.cursor/rules/` 目录
- 在状态栏查看是否显示 "Rules loaded"
- 如未加载，重启 Cursor

### 3. 测试 AI 助手

按 `Cmd/Ctrl+K` 并输入：

```
"为这个 MCP 服务器添加一个新的工具，用于计算两个数字的最大公约数"
```

AI 会自动：
1. 在 `server/tools/` 目录创建新文件
2. 生成完整的工具代码
3. 添加类型注解和文档
4. 注册到 MCP 服务器

### 4. 继续开发

```
"为刚才的工具生成单元测试"
"添加一个资源，用于获取当前系统的 Python 版本信息"
"创建一个提示模板，用于代码重构建议"
```

## 🧪 步骤 6：运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_tools.py -v

# 生成测试覆盖率报告
python -m pytest tests/ --cov=server --cov-report=html
```

预期输出：
```
======================== test session starts ========================
collected 12 items

tests/test_tools.py::TestCalculatorTools::test_add ✓
tests/test_tools.py::TestCalculatorTools::test_subtract ✓
...
======================== 12 passed in 0.02s ========================
```

## 🐳 步骤 7：Docker 部署 (可选)

### 构建镜像

```bash
# 构建生产镜像
docker build -t my-mcp-server .

# 查看镜像大小
docker images my-mcp-server
```

### 运行容器

```bash
# 开发环境
docker run -p 8000:8000 \
  -e ENVIRONMENT=development \
  my-mcp-server

# 生产环境 (自动多进程)
docker run -d \
  --name mcp-server \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  my-mcp-server
```

### 验证容器

```bash
# 检查容器状态
docker ps

# 查看日志
docker logs mcp-server

# 测试健康检查
curl http://localhost:8000/health
```

## 🎯 下一步

### 开发你的 MCP 服务器

1. **自定义工具**：在 `server/tools/` 添加业务逻辑
2. **添加资源**：在 `server/resources/` 提供数据接口
3. **创建提示**：在 `server/prompts/` 定义 AI 交互模板
4. **扩展 API**：在 `server/routes/` 添加自定义端点

### 学习更多

- 📚 [Cursor 使用指南](CURSOR_GUIDE.md) - 深度使用 AI 开发
- 🏗️ [最佳实践](BEST_PRACTICES.md) - 生产级开发规范
- 🐳 [Docker 优化](DOCKER_OPTIMIZATION.md) - 高性能部署
- 📊 [监控运维](MONITORING.md) - 生产环境监控

### 获取帮助

- 💬 [GitHub Discussions](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/discussions)
- 🐛 [问题反馈](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/issues)
- 📧 **邮箱**: toxingwang@gmail.com

## 🎉 常见问题

### Q: 为什么选择 Streamable HTTP 而不是 stdio？

**A**: 
- **stdio**: 适合本地开发和调试
- **Streamable HTTP**: 适合生产部署，支持负载均衡、监控等

### Q: 如何自定义端口？

**A**: 
```bash
# 方法 1: 命令行参数
python run.py --port 9000

# 方法 2: 环境变量
export PORT=9000
python run.py

# 方法 3: 修改 .env 文件
echo "PORT=9000" > .env
```

### Q: 如何添加环境变量？

**A**: 
```bash
# 复制示例配置
cp env.example .env

# 编辑配置文件
vim .env
```

### Q: Cursor AI 规则没有生效？

**A**: 
1. 确保 `.cursor/rules/` 目录存在
2. 重启 Cursor IDE
3. 检查 Cursor 设置中的规则配置
4. 更新到最新版本的 Cursor

---

**🎉 恭喜！你已经成功启动了第一个 MCP 服务器！**

现在可以开始使用 Cursor AI 快速开发你的 MCP 应用了。 