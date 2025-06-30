"""
主 MCP 服务器实例

使用 FastMCP 框架创建高性能的 MCP 服务器，支持 Streamable HTTP 传输。
集成所有工具、资源和提示模板。
"""

import logging
from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request

from .config import settings
from .prompts import register_prompts
from .resources import register_resources
from .routes import register_routes
from .tools import register_tools

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format
)
logger = logging.getLogger(__name__)

# 创建 FastMCP 实例
mcp = FastMCP(
    name=settings.app_name,
    stateless_http=settings.stateless_http,
)

# 注册所有组件
register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)


# ---------- 健康检查端点 ----------
@mcp.custom_route(path="/health", methods=["GET"])
async def health_check(_: Request) -> JSONResponse:
    """健康检查端点"""
    return JSONResponse({
        "status": "healthy",
        "version": settings.version,
        "app_name": settings.app_name,
        "environment": settings.environment,
        "transport": settings.transport
    })


@mcp.custom_route(path="/info", methods=["GET"])
async def server_info(_: Request) -> JSONResponse:
    """服务器信息端点"""
    return JSONResponse({
        "name": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "mcp_version": "1.10.1",
        "transport": settings.transport,
        "capabilities": {
            "tools": True,
            "resources": True,
            "prompts": True,
            "logging": True,
        }
    })


# ---------- 静态文件服务 ----------
def mount_static(app):
    """挂载静态文件服务"""
    static_dir = Path(__file__).parent.parent / "static"
    static_dir.mkdir(exist_ok=True)

    # 创建示例静态文件
    index_file = static_dir / "index.html"
    if not index_file.exists():
        index_file.write_text("""
<!DOCTYPE html>
<html>
<head>
    <title>Awesome MCP Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { color: #333; }
        .info { background: #f5f5f5; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1 class="header">🚀 Awesome MCP Server</h1>
    <div class="info">
        <p><strong>Status:</strong> Running</p>
        <p><strong>Version:</strong> """ + settings.version + """</p>
        <p><strong>Environment:</strong> """ + settings.environment + """</p>
        <p><strong>Transport:</strong> """ + settings.transport + """</p>
    </div>
    <h2>Endpoints</h2>
    <ul>
        <li><a href="/health">Health Check</a></li>
        <li><a href="/info">Server Info</a></li>
        <li><a href="/mcp">MCP Endpoint</a></li>
    </ul>
</body>
</html>
        """)

    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"Static files mounted at /static from {static_dir}")


# ---------- 注册自定义路由 ----------
register_routes(mcp)


def create_app():
    """创建 FastAPI 应用实例 - 支持 uvicorn factory 模式"""
    app = mcp.streamable_http_app()
    mount_static(app)

    logger.info(f"MCP Server '{settings.app_name}' initialized")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Transport: {settings.transport}")
    logger.info(f"Stateless HTTP: {settings.stateless_http}")

    return app


# 为 uvicorn factory 模式提供应用工厂函数
def app_factory():
    """应用工厂函数 - 用于 uvicorn --factory 模式"""
    return create_app()


def main():
    """主函数 - 用于命令行启动"""
    import os

    # 直接从环境变量读取配置，确保获取最新值
    transport = os.getenv("TRANSPORT", "streamable-http")
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "INFO")

    if transport == "streamable-http":
        # HTTP 模式
        import uvicorn
        app = create_app()
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level=log_level.lower()
        )
    else:
        # stdio 模式
        mcp.run(transport=transport)


if __name__ == "__main__":
    main()
