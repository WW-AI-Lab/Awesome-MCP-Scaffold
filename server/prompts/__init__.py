"""
MCP 提示模块

包含所有 MCP 提示模板的实现和注册逻辑。
提示模板为 LLM 交互提供可重用的指令模式。
"""

import logging

from mcp.server.fastmcp import FastMCP

from .code_review import register_code_prompts
from .data_analysis import register_analysis_prompts

logger = logging.getLogger(__name__)


def register_prompts(mcp: FastMCP) -> None:
    """注册所有 MCP 提示模板"""
    logger.info("Registering MCP prompts...")

    # 注册代码审查提示
    register_code_prompts(mcp)

    # 注册数据分析提示
    register_analysis_prompts(mcp)

    logger.info("All MCP prompts registered successfully")
