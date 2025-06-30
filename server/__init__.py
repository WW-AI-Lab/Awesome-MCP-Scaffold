"""
Awesome MCP Server

这个包包含了 MCP 服务器的所有核心组件：
- tools: MCP 工具实现
- resources: MCP 资源实现
- prompts: MCP 提示模板
- routes: 自定义 HTTP 路由

主要模块：
- main: 主服务器实例
- config: 配置管理
"""

__version__ = "1.0.0"
__author__ = "WW-AI-Lab"
__email__ = "toxingwang@gmail.com"

from .main import mcp

__all__ = ['mcp']
