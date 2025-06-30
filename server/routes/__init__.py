"""
自定义路由模块

包含所有自定义 HTTP 路由的实现和注册逻辑。
这些路由提供标准 REST API 端点，补充 MCP 功能。
"""

import logging

from mcp.server.fastmcp import FastMCP

from .api_routes import register_api_routes

logger = logging.getLogger(__name__)


def register_routes(mcp: FastMCP) -> None:
    """注册所有自定义路由"""
    logger.info("Registering custom routes...")

    # 注册 API 路由
    register_api_routes(mcp)

    logger.info("All custom routes registered successfully")
