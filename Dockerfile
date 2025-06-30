# Awesome MCP Scaffold Dockerfile
# 多阶段构建，优化镜像大小和安全性
# 标签信息
LABEL maintainer="WW-AI-Lab <toxingwang@gmail.com>"
LABEL version="1.0.0"
LABEL description="Awesome MCP Scaffold - Production-ready MCP Server"
LABEL org.opencontainers.image.source="https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold" 

# 构建阶段
FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 复制依赖文件
COPY requirements.txt pyproject.toml ./

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 升级 pip 并安装依赖
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 运行阶段
FROM python:3.11-slim as runtime

# 创建非 root 用户
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# 安装运行时系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制应用代码
COPY server/ ./server/
COPY tests/ ./tests/
COPY docs/ ./docs/
COPY Makefile ./
COPY env.example ./
COPY docker-entrypoint.sh ./

# 创建必要的目录并设置权限
RUN mkdir -p workspace logs static && \
    chmod +x docker-entrypoint.sh && \
    chown -R mcpuser:mcpuser /app

# 切换到非 root 用户
USER mcpuser

# 设置环境变量
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production
ENV HOST=0.0.0.0
ENV PORT=8000
ENV TRANSPORT=streamable-http

# 生产级性能配置
ENV UVICORN_WORKERS=4
ENV UVICORN_WORKER_CLASS=uvicorn.workers.UvicornWorker
ENV UVICORN_MAX_REQUESTS=1000
ENV UVICORN_MAX_REQUESTS_JITTER=100
ENV UVICORN_PRELOAD_APP=true
ENV UVICORN_KEEPALIVE=2

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 生产级启动命令 - 使用智能入口脚本
CMD ["./docker-entrypoint.sh"]