"""
MCP 资源模块

包含所有 MCP 资源的实现和注册逻辑。
资源提供只读数据访问，类似于 REST API 的 GET 端点。
"""

import logging

from mcp.server.fastmcp import FastMCP

from .config_data import register_config_resources
from .system_info import register_system_resources

logger = logging.getLogger(__name__)


def register_resources(mcp: FastMCP) -> None:
    """注册所有 MCP 资源"""
    logger.info("Registering MCP resources...")

    # 注册系统信息资源
    register_system_resources(mcp)

    # 注册配置数据资源
    register_config_resources(mcp)

    logger.info("All MCP resources registered successfully")
