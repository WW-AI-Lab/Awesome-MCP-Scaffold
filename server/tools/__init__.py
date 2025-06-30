"""
MCP 工具模块

包含所有 MCP 工具的实现和注册逻辑。
工具允许 LLM 执行各种操作和计算。
"""

import logging

from mcp.server.fastmcp import FastMCP

from .calculator import register_calculator_tools
from .file_operations import register_file_tools
from .text_processing import register_text_tools

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:
    """注册所有 MCP 工具"""
    logger.info("Registering MCP tools...")

    # 注册计算器工具
    register_calculator_tools(mcp)

    # 注册文本处理工具
    register_text_tools(mcp)

    # 注册文件操作工具
    register_file_tools(mcp)

    logger.info("All MCP tools registered successfully")
