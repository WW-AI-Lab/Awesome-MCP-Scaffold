"""
API 路由模块

提供标准 REST API 端点，补充 MCP 协议功能。
"""

from datetime import datetime

from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request

from ..config import settings


def register_api_routes(mcp: FastMCP) -> None:
    """注册 API 路由"""

    @mcp.custom_route(path="/api/v1/tools", methods=["GET"])
    async def list_tools_api(_: Request) -> JSONResponse:
        """获取所有可用工具的列表 (REST API)"""
        # 这里应该动态获取实际注册的工具
        tools = [
            {
                "name": "add",
                "title": "Add Numbers",
                "description": "Add two numbers together",
                "category": "calculator"
            },
            {
                "name": "calculate_bmi",
                "title": "Calculate BMI",
                "description": "Calculate Body Mass Index",
                "category": "calculator"
            },
            {
                "name": "count_words",
                "title": "Count Words",
                "description": "Count words in text",
                "category": "text_processing"
            },
            {
                "name": "list_directory",
                "title": "List Directory",
                "description": "List files and directories",
                "category": "file_operations"
            }
        ]

        return JSONResponse({
            "tools": tools,
            "count": len(tools),
            "timestamp": datetime.now().isoformat()
        })

    @mcp.custom_route(path="/api/v1/resources", methods=["GET"])
    async def list_resources_api(_: Request) -> JSONResponse:
        """获取所有可用资源的列表 (REST API)"""
        resources = [
            {
                "uri": "system://info",
                "title": "System Information",
                "description": "Get basic system information"
            },
            {
                "uri": "system://memory",
                "title": "Memory Usage",
                "description": "Get current memory usage information"
            },
            {
                "uri": "config://app",
                "title": "Application Configuration",
                "description": "Get current application configuration"
            },
            {
                "uri": "config://user/{user_id}",
                "title": "User Configuration",
                "description": "Get user-specific configuration",
                "template": True
            }
        ]

        return JSONResponse({
            "resources": resources,
            "count": len(resources),
            "timestamp": datetime.now().isoformat()
        })

    @mcp.custom_route(path="/api/v1/prompts", methods=["GET"])
    async def list_prompts_api(_: Request) -> JSONResponse:
        """获取所有可用提示模板的列表 (REST API)"""
        prompts = [
            {
                "name": "code_review",
                "title": "Code Review",
                "description": "Generate a prompt for comprehensive code review"
            },
            {
                "name": "bug_analysis",
                "title": "Bug Analysis",
                "description": "Generate a prompt for bug analysis and debugging"
            },
            {
                "name": "data_analysis",
                "title": "Data Analysis",
                "description": "Generate a prompt for comprehensive data analysis"
            }
        ]

        return JSONResponse({
            "prompts": prompts,
            "count": len(prompts),
            "timestamp": datetime.now().isoformat()
        })

    @mcp.custom_route(path="/api/v1/status", methods=["GET"])
    async def server_status(_: Request) -> JSONResponse:
        """获取服务器状态信息"""
        return JSONResponse({
            "status": "running",
            "app_name": settings.app_name,
            "version": settings.version,
            "environment": settings.environment,
            "transport": settings.transport,
            "uptime": "N/A",  # 这里可以计算实际运行时间
            "timestamp": datetime.now().isoformat()
        })

    @mcp.custom_route(path="/api/v1/convert", methods=["POST"])
    async def data_converter(request: Request) -> JSONResponse:
        """通用数据转换端点"""
        try:
            data = await request.json()
            operation = data.get("operation", "echo")
            payload = data.get("data", {})

            if operation == "echo":
                result = payload
            elif operation == "uppercase":
                if isinstance(payload, str):
                    result = payload.upper()
                else:
                    result = {"error": "Payload must be a string for uppercase operation"}
            elif operation == "reverse":
                if isinstance(payload, str):
                    result = payload[::-1]
                elif isinstance(payload, list):
                    result = payload[::-1]
                else:
                    result = {"error": "Payload must be string or list for reverse operation"}
            else:
                result = {"error": f"Unknown operation: {operation}"}

            return JSONResponse({
                "operation": operation,
                "input": payload,
                "output": result,
                "timestamp": datetime.now().isoformat()
            })

        except Exception as e:
            return JSONResponse(
                {"error": str(e), "timestamp": datetime.now().isoformat()},
                status_code=400
            )

    @mcp.custom_route(path="/api/v1/metrics", methods=["GET"])
    async def server_metrics(_: Request) -> JSONResponse:
        """获取服务器指标 (简化版)"""
        # 这里可以集成实际的指标收集
        return JSONResponse({
            "metrics": {
                "requests_total": 0,
                "requests_per_second": 0,
                "average_response_time": 0,
                "active_connections": 0,
                "memory_usage": "N/A",
                "cpu_usage": "N/A"
            },
            "timestamp": datetime.now().isoformat()
        })
