# 📖 5-Minute Quick Start Guide

> From zero to running your first MCP server in 5 minutes

## 🎯 Before You Start

### Environment Requirements
- **Python 3.10+** (recommended 3.11+)
- **Cursor IDE** (highly recommended for best AI development experience)
- **Git** (for cloning the scaffold)

### Optional Tools
- **Docker** (for containerized deployment)
- **uv** (faster Python package manager)

## 🚀 Step 1: Get the Scaffold

```bash
# Clone scaffold to local
git clone https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold.git my-mcp-server
cd my-mcp-server

# Rename to your project
# Optional: Remove .git directory and reinitialize
rm -rf .git
git init
```

## 🔧 Step 2: Environment Setup

### Option A: Using pip (recommended for beginners)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: Using uv (faster)

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project and install dependencies
uv sync
```

## ⚡ Step 3: Start Server

### Development Mode (stdio)

```bash
# Simplest startup method
python run.py

# Using FastMCP CLI (recommended for development)
fastmcp dev run.py
```

### HTTP Mode (recommended)

```bash
# Start HTTP server
python run.py --transport streamable-http --port 8000

# Run in background
python run.py --transport streamable-http --port 8000 &
```

## ✅ Step 4: Verify Functionality

### Basic Health Check

```bash
# Check server status
curl http://localhost:8000/health

# Expected output:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "app_name": "Awesome MCP Server",
#   "environment": "development"
# }
```

### View Server Information

```bash
# Get detailed information
curl http://localhost:8000/info | python -m json.tool

# Expected output:
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

### Test Built-in Tools

```bash
# View available tools
curl http://localhost:8000/api/tools

# Test calculator tool
curl -X POST http://localhost:8000/api/tools/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5}'
```

## 🤖 Step 5: Cursor AI Development

### 1. Open Project in Cursor

```bash
# Open in Cursor
cursor .

# Or manually open Cursor, then open project folder
```

### 2. Verify AI Rules Loading

- Cursor will automatically recognize `.cursor/rules/` directory
- Check status bar for "Rules loaded" display
- If not loaded, restart Cursor

### 3. Test AI Assistant

Press `Cmd/Ctrl+K` and input:

```
"Add a new tool to this MCP server for calculating the greatest common divisor of two numbers"
```

AI will automatically:
1. Create new file in `server/tools/` directory
2. Generate complete tool code
3. Add type annotations and documentation
4. Register to MCP server

### 4. Continue Development

```
"Generate unit tests for the tool just created"
"Add a resource to get current system's Python version information"
"Create a prompt template for code refactoring suggestions"
```

## 🧪 Step 6: Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific tests
python -m pytest tests/test_tools.py -v

# Generate test coverage report
python -m pytest tests/ --cov=server --cov-report=html
```

Expected output:
```
======================== test session starts ========================
collected 12 items

tests/test_tools.py::TestCalculatorTools::test_add ✓
tests/test_tools.py::TestCalculatorTools::test_subtract ✓
...
======================== 12 passed in 0.02s ========================
```

## 🐳 Step 7: Docker Deployment (Optional)

### Build Image

```bash
# Build production image
docker build -t my-mcp-server .

# View image size
docker images my-mcp-server
```

### Run Container

```bash
# Development environment
docker run -p 8000:8000 \
  -e ENVIRONMENT=development \
  my-mcp-server

# Production environment (automatic multi-process)
docker run -d \
  --name mcp-server \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  my-mcp-server
```

### Verify Container

```bash
# Check container status
docker ps

# View logs
docker logs mcp-server

# Test health check
curl http://localhost:8000/health
```

## 🎯 Next Steps

### Develop Your MCP Server

1. **Custom tools**: Add business logic in `server/tools/`
2. **Add resources**: Provide data interfaces in `server/resources/`
3. **Create prompts**: Define AI interaction templates in `server/prompts/`
4. **Extend API**: Add custom endpoints in `server/routes/`

### Learn More

- 📚 [Cursor Usage Guide](CURSOR_GUIDE_EN.md) - Deep dive into AI development
- 🏗️ [Best Practices](BEST_PRACTICES_EN.md) - Production-grade development standards
- 🐳 [Docker Optimization](DOCKER_OPTIMIZATION_EN.md) - High-performance deployment
- 📊 [Monitoring & Operations](MONITORING_EN.md) - Production environment monitoring

### Get Help

- 💬 [GitHub Discussions](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/discussions)
- 🐛 [Issue Reports](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/issues)
- 📧 **Email**: toxingwang@gmail.com

## 🎉 FAQ

### Q: Why choose Streamable HTTP over stdio?

**A**: 
- **stdio**: Suitable for local development and debugging
- **Streamable HTTP**: Suitable for production deployment, supports load balancing, monitoring, etc.

### Q: How to customize port?

**A**: 
```bash
# Method 1: Command line argument
python run.py --port 9000

# Method 2: Environment variable
export PORT=9000
python run.py

# Method 3: Modify .env file
echo "PORT=9000" > .env
```

### Q: How to add environment variables?

**A**: 
```bash
# Copy example configuration
cp env.example .env

# Edit configuration file
vim .env
```

### Q: Cursor AI rules not taking effect?

**A**: 
1. Ensure `.cursor/rules/` directory exists
2. Restart Cursor IDE
3. Check rule configuration in Cursor settings
4. Update to latest version of Cursor

---

**🎉 Congratulations! You have successfully started your first MCP server!**

Now you can start using Cursor AI to rapidly develop your MCP applications. 