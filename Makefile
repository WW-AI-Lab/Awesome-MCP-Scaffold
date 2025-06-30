# Awesome MCP Scaffold Makefile
# 提供常用的开发和部署命令

.PHONY: help install dev test lint format clean build run docs deploy

# 默认目标
help:
	@echo "Awesome MCP Scaffold - 可用命令："
	@echo ""
	@echo "开发命令："
	@echo "  install     安装依赖"
	@echo "  dev         启动开发服务器"
	@echo "  test        运行测试"
	@echo "  lint        代码检查"
	@echo "  format      代码格式化"
	@echo "  clean       清理临时文件"
	@echo ""
	@echo "构建和部署："
	@echo "  build       构建应用"
	@echo "  run         运行生产服务器"
	@echo "  docs        生成文档"
	@echo "  deploy      部署到生产环境"
	@echo ""

# 安装依赖
install:
	@echo "📦 安装 Python 依赖..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ 依赖安装完成"

# 开发环境安装
install-dev: install
	@echo "🔧 安装开发依赖..."
	pip install pytest pytest-asyncio pytest-cov ruff mypy pre-commit
	pre-commit install
	@echo "✅ 开发环境配置完成"

# 启动开发服务器
dev:
	@echo "🚀 启动开发服务器..."
	python -m server.main

# 使用 FastMCP CLI 启动开发服务器
dev-fastmcp:
	@echo "🚀 使用 FastMCP CLI 启动开发服务器..."
	fastmcp dev server/main.py

# 运行测试
test:
	@echo "🧪 运行测试..."
	pytest tests/ -v --cov=server --cov-report=html --cov-report=term

# 运行特定测试
test-tools:
	pytest tests/test_tools.py -v

test-integration:
	pytest tests/ -k "integration" -v

# 代码检查
lint:
	@echo "🔍 代码检查..."
	ruff check server/ tests/
	mypy server/

# 代码格式化
format:
	@echo "✨ 代码格式化..."
	ruff format server/ tests/
	ruff check --fix server/ tests/

# 清理临时文件
clean:
	@echo "🧹 清理临时文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/
	@echo "✅ 清理完成"

# 构建应用
build:
	@echo "🏗️ 构建应用..."
	python -m build
	@echo "✅ 构建完成"

# 运行生产服务器
run:
	@echo "🚀 启动生产服务器..."
	ENVIRONMENT=production python -m server.main

# 使用 uvicorn 运行
run-uvicorn:
	@echo "🚀 使用 uvicorn 启动服务器..."
	uvicorn server.main:create_app --factory --host 0.0.0.0 --port 8000

# 生成文档
docs:
	@echo "📚 生成文档..."
	# 这里可以添加文档生成命令，如 Sphinx
	@echo "✅ 文档生成完成"

# Docker 构建
docker-build:
	@echo "🐳 构建 Docker 镜像..."
	docker build -t awesome-mcp-scaffold .

# Docker 运行
docker-run:
	@echo "🐳 运行 Docker 容器..."
	docker run -p 8000:8000 awesome-mcp-scaffold

# 部署到生产环境
deploy:
	@echo "🚀 部署到生产环境..."
	# 这里添加具体的部署命令
	@echo "✅ 部署完成"

# 健康检查
health:
	@echo "🏥 检查服务器健康状态..."
	curl -s http://localhost:8000/health | python -m json.tool

# 查看服务器信息
info:
	@echo "ℹ️ 获取服务器信息..."
	curl -s http://localhost:8000/info | python -m json.tool

# 查看 API 端点
api:
	@echo "🔗 查看可用 API 端点..."
	@echo "Tools: http://localhost:8000/api/v1/tools"
	@echo "Resources: http://localhost:8000/api/v1/resources"
	@echo "Prompts: http://localhost:8000/api/v1/prompts"
	@echo "Status: http://localhost:8000/api/v1/status"

# 初始化项目
init:
	@echo "🎉 初始化 Awesome MCP Scaffold 项目..."
	cp env.example .env
	mkdir -p workspace logs
	make install-dev
	@echo "✅ 项目初始化完成！"
	@echo ""
	@echo "下一步："
	@echo "1. 编辑 .env 文件配置环境变量"
	@echo "2. 运行 'make dev' 启动开发服务器"
	@echo "3. 访问 http://localhost:8000 查看服务器状态"

# 完整的开发工作流
workflow: clean format lint test
	@echo "🎯 开发工作流完成！" 