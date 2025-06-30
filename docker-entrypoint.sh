#!/bin/bash
set -e

# Docker 入口脚本 - 支持灵活的生产环境配置

# 默认配置
DEFAULT_HOST=${HOST:-0.0.0.0}
DEFAULT_PORT=${PORT:-8000}
DEFAULT_WORKERS=${UVICORN_WORKERS:-4}
DEFAULT_WORKER_CLASS=${UVICORN_WORKER_CLASS:-uvicorn.workers.UvicornWorker}
DEFAULT_MAX_REQUESTS=${UVICORN_MAX_REQUESTS:-1000}
DEFAULT_MAX_REQUESTS_JITTER=${UVICORN_MAX_REQUESTS_JITTER:-100}
DEFAULT_KEEPALIVE=${UVICORN_KEEPALIVE:-2}
DEFAULT_LOG_LEVEL=${LOG_LEVEL:-info}

# 根据容器资源自动调整 worker 数量
if [ -z "$UVICORN_WORKERS" ]; then
    # 获取 CPU 核心数 (兼容 Linux 和 macOS)
    if command -v nproc >/dev/null 2>&1; then
        CPU_CORES=$(nproc)
    elif command -v sysctl >/dev/null 2>&1; then
        CPU_CORES=$(sysctl -n hw.ncpu)
    else
        CPU_CORES=2  # 默认值
    fi
    
    # 使用公式: workers = (2 * CPU_cores) + 1，但最少2个，最多8个
    CALCULATED_WORKERS=$((2 * CPU_CORES + 1))
    if [ $CALCULATED_WORKERS -lt 2 ]; then
        CALCULATED_WORKERS=2
    elif [ $CALCULATED_WORKERS -gt 8 ]; then
        CALCULATED_WORKERS=8
    fi
    DEFAULT_WORKERS=$CALCULATED_WORKERS
fi

echo "🚀 Starting Awesome MCP Server..."
echo "📊 Configuration:"
echo "   Host: $DEFAULT_HOST"
echo "   Port: $DEFAULT_PORT"
echo "   Workers: $DEFAULT_WORKERS"
echo "   Worker Class: $DEFAULT_WORKER_CLASS"
echo "   Max Requests: $DEFAULT_MAX_REQUESTS"
echo "   Keep Alive: $DEFAULT_KEEPALIVE"
echo "   Log Level: $DEFAULT_LOG_LEVEL"
echo "   Environment: ${ENVIRONMENT:-production}"

# 检查是否为开发模式
if [ "$ENVIRONMENT" = "development" ]; then
    echo "🔧 Development mode detected"
    exec uvicorn server.main:create_app \
        --factory \
        --host "$DEFAULT_HOST" \
        --port "$DEFAULT_PORT" \
        --reload \
        --log-level debug \
        --access-log
else
    echo "🏭 Production mode detected"
    exec uvicorn server.main:create_app \
        --factory \
        --host "$DEFAULT_HOST" \
        --port "$DEFAULT_PORT" \
        --workers "$DEFAULT_WORKERS" \
        --worker-class "$DEFAULT_WORKER_CLASS" \
        --max-requests "$DEFAULT_MAX_REQUESTS" \
        --max-requests-jitter "$DEFAULT_MAX_REQUESTS_JITTER" \
        --preload \
        --keepalive "$DEFAULT_KEEPALIVE" \
        --access-log \
        --log-level "$DEFAULT_LOG_LEVEL"
fi 