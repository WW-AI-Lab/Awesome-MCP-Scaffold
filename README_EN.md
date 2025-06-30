# 🚀 Awesome-MCP-Scaffold

> **Production-Grade MCP Server Development Scaffold - Fast Development Solution Optimized for Cursor IDE**

English | [中文](README.md)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-v1.10.1-green.svg)](https://modelcontextprotocol.io)
[![Streamable HTTP](https://img.shields.io/badge/Transport-Streamable%20HTTP-orange.svg)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Production%20Ready-blue.svg)](docs/DOCKER_OPTIMIZATION_EN.md)

## 🎯 Project Positioning

**Awesome-MCP-Scaffold** is a **ready-to-use MCP server development scaffold** that enables you to:

- 🚀 **5-minute startup**: Complete MCP server from zero to running
- 🤖 **10-minute MCP development**: Built-in prompts and examples, complete MCP Server tools development with one sentence based on Cursor IDE
- 🏭 **Production-grade architecture**: Verified high-performance deployment solution
- 📚 **Built-in best practices**: Following official MCP SDK v1.10.1 specifications

## ✨ Core Advantages

### 🔥 Optimized for Cursor
- **Intelligent rule system**: Built-in user Rules `Cursor_User_Rules.md` and 3 sets of project `.cursor/rules` configurations
- **AI code generation**: Automatically generate Tools, Resources, Prompts with one sentence, and auto-generate test cases
- **Context awareness**: AI assistant understands MCP development patterns
- **Automatic error fixing**: Intelligently identify and fix common issues

### ⚡ Complete Out-of-the-Box Functionality
- **12+ example tools**: Calculator, text processing, file operations, etc.
- **Multiple resource types**: System information, configuration data, etc.
- **Prompt templates**: Code review, data analysis and other scenarios
- **REST API endpoints**: Support for complete HTTP API integration, convenient for platforms that don't support MCP

### 🏗️ Production-Grade Architecture
- **Streamable HTTP first**: Latest transport protocol, 3-5x performance improvement
- **Docker optimized**: Multi-process deployment, intelligent resource management
- **Load balancing**: Nginx configuration, supports horizontal scaling
- **Monitoring integration**: Prometheus + Grafana out-of-the-box

## 🚀 5-Minute Quick Start

### 1. Clone the Scaffold

```bash
# Create new project using scaffold
git clone https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold.git my-mcp-server
cd my-mcp-server

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Development Server

```bash
# Development mode (stdio)
python run.py

# HTTP mode (recommended)
python run.py --transport streamable-http --port 8000

# Using FastMCP CLI
fastmcp dev run.py
```

### 3. Verify Server

```bash
# Health check
curl http://localhost:8000/health

# View server information
curl http://localhost:8000/info

# Test tools list
curl http://localhost:8000/api/tools
```

### 4. Develop in Cursor

1. **Open project**: Open project folder in Cursor
2. **AI assistant activation**: Cursor automatically loads `.cursor/rules` configuration
3. **Start developing**: Press `Cmd/Ctrl+K` input requirements, AI automatically generates code

## 📁 Scaffold Structure

```
awesome-mcp-scaffold/
├── 🎯 Core Architecture
│   ├── server/                 # MCP server core
│   │   ├── main.py            # FastMCP main instance
│   │   ├── config.py          # Configuration management
│   │   ├── tools/             # Tool implementations (12+ examples)
│   │   ├── resources/         # Resource implementations
│   │   ├── prompts/           # Prompt templates
│   │   └── routes/            # REST API routes
│   └── run.py                 # Entry point
│
├── 🤖 Cursor Integration
│   └── .cursor/rules/         # AI rule configurations
│       ├── mcp-development-guide.mdc
│       ├── streamable-http-production.mdc
│       └── mcp-testing-patterns.mdc
│
├── 🏭 Production Deployment
│   ├── Dockerfile             # Production-grade container config
│   ├── docker-compose.yml     # Multi-environment deployment
│   ├── docker-entrypoint.sh   # Intelligent startup script
│   └── deploy/                # Deployment configurations
│       ├── nginx/             # Load balancing
│       └── kubernetes/        # K8s configurations
│
├── 📚 Documentation Guide
│   ├── docs/GETTING_STARTED_EN.md
│   ├── docs/CURSOR_GUIDE_EN.md
│   ├── docs/DOCKER_OPTIMIZATION_EN.md
│   └── docs/BEST_PRACTICES_EN.md
│
└── 🧪 Testing Verification
    ├── tests/                 # Complete test suite
    ├── Makefile              # Development commands
    └── pyproject.toml        # Project configuration
```

## 🤖 Cursor AI Development Experience

### Intelligent Code Generation

**Create new tool** - Press `Cmd/Ctrl+K` in Cursor:
```
"Create a weather query tool that supports city name and coordinate queries, work step by step to achieve the goal"
```

AI automatically generates:
```python
@mcp.tool(title="Weather Query", description="Query weather by city or coordinates")
def get_weather(location: str, units: str = "metric") -> Dict[str, Any]:
    """Query current weather information."""
    # Complete implementation code...
```

**Add resource** - Continue conversation:
```
"Add a configuration resource for the weather tool, supporting API key management"
```

**Generate tests** - One-click generation:
```
"Generate complete test cases for the weather tool"
```

### Three Professional Rule Sets

| Rule File | Purpose | Trigger Scenario |
|-----------|---------|------------------|
| `mcp-development-guide.mdc` | MCP development guidance | Developing Tools/Resources/Prompts |
| `streamable-http-production.mdc` | Production deployment optimization | Deployment configuration and performance optimization |
| `mcp-testing-patterns.mdc` | Testing best practices | Writing and optimizing test code |

## 🏭 Production-Grade Deployment

### Docker One-Click Deployment

```bash
# Build production image
docker build -t my-mcp-server .

# Start production server (automatic multi-process)
docker run -d \
  --name mcp-server \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  my-mcp-server
```

### Performance Benchmarks (Verified)

| Deployment Mode | QPS | Latency(P99) | Memory Usage | Use Case |
|-----------------|-----|--------------|--------------|----------|
| Development | 1,000 | 50ms | 100MB | Local development |
| Production | 3,500+ | 30ms | 300MB | Production environment |
| Load Balanced | 10,000+ | 25ms | 1GB | High concurrency |

### Docker Compose Full Stack

```bash
# Start complete service stack
docker-compose up -d

# Includes: MCP Server + Nginx + Prometheus + Grafana
```

## 📊 Built-in Example Features

### 🛠️ Tools
- **Calculator**: Basic math operations, BMI calculation, percentage calculation
- **Text processing**: Word count, format conversion, regex extraction
- **File operations**: Safe file read/write, JSON processing

### 📡 Resources
- **System information**: CPU, memory, disk status monitoring
- **Configuration data**: Application configuration, version information management

### 💬 Prompts
- **Code review**: Quality analysis, bug detection, performance optimization
- **Data analysis**: Statistical analysis, predictive modeling, quality assessment

### 🌐 REST API
- `/health` - Health check
- `/info` - Server information
- `/api/tools` - Tools list
- `/api/resources` - Resources list

## 🧪 Verification and Testing

### Automated Test Suite
```bash
# Run complete tests
make test

# Code quality check
make lint

# Test coverage
make coverage
```

### Manual Verification Steps
```bash
# 1. Functional testing
curl http://localhost:8000/health
curl http://localhost:8000/api/tools

# 2. MCP protocol testing
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python run.py

# 3. Performance testing
ab -n 1000 -c 10 http://localhost:8000/health
```

## 📚 Learning Resources

### Beginner Guide
- 📖 [5-Minute Quick Start](docs/GETTING_STARTED_EN.md)
- 🎯 [Cursor Usage Guide](docs/CURSOR_GUIDE_EN.md)
- 🏗️ [Best Practices](docs/BEST_PRACTICES_EN.md)

### Advanced Guide
- 🐳 [Docker Production Optimization](docs/DOCKER_OPTIMIZATION_EN.md)
- 🚀 [Performance Tuning Guide](docs/PERFORMANCE_TUNING_EN.md)
- 📊 [Monitoring and Operations](docs/MONITORING_EN.md)

### Official Resources
- 🌐 [MCP Official Documentation](https://modelcontextprotocol.io)
- 📦 [Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 🎉 Success Stories

Production projects built with this scaffold:

- **[any2markdown](https://github.com/WW-AI-Lab/any2markdown)** - A high-performance document conversion server that supports both Model Context Protocol (MCP) and RESTful API interfaces. Converts PDF, Word and Excel documents to Markdown format, with advanced features like image extraction, header/footer removal and batch processing
- **[azure-gpt-image](https://github.com/WW-AI-Lab/azure-gpt-image)** - A Model Context Protocol (MCP) server based on Azure OpenAI gpt-image-1 model, implemented using the official MCP SDK's Streamable HTTP Transport, providing powerful image generation and editing capabilities for AI assistants
- **[jinja2-mcp-server](https://github.com/WW-AI-Lab/jinja2-mcp-server)** - A Model Context Protocol (MCP) server based on Jinja2 templates, implemented using the official MCP SDK's Streamable HTTP Transport, providing powerful template rendering capabilities for AI assistants

## 🤝 Community Support

### Getting Help
- 💬 [GitHub Discussions](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/discussions)
- 🐛 [Issue Reports](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/issues)
- 📧 **Email**: toxingwang@gmail.com

### Contribution Guide
- 🔄 [Contribution Process](CONTRIBUTING.md)
- 📋 [Development Standards](docs/DEVELOPMENT_EN.md)
- 🧪 [Testing Guide](docs/TESTING_EN.md)

## 📄 License

This project is licensed under the [MIT License](LICENSE) - free for commercial and open source projects.

## 🙏 Acknowledgments

Thanks to the following projects and communities for their support:

- **[Anthropic](https://anthropic.com)** - Creator of the MCP protocol
- **[Cursor](https://cursor.sh)** - AI-powered code editor
- **[WW-AI-Lab](https://github.com/WW-AI-Lab)** - AI Lab community

---

**🚀 Start your MCP server development journey now!**

If this scaffold helps you, please give us a Star⭐️ 