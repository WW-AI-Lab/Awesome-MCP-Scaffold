"""
配置数据资源模块

提供应用配置和元数据的 MCP 资源。
"""

import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP

from ..config import settings


def register_config_resources(mcp: FastMCP) -> None:
    """注册配置数据相关的资源"""

    @mcp.resource("config://app", title="Application Configuration")
    def app_config() -> str:
        """Get current application configuration."""
        config_data = {
            "app_name": settings.app_name,
            "version": settings.version,
            "environment": settings.environment,
            "debug": settings.debug,
            "host": settings.host,
            "port": settings.port,
            "transport": settings.transport,
            "mcp_mount_path": settings.mcp_mount_path,
            "stateless_http": settings.stateless_http,
            "log_level": settings.log_level,
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(config_data, indent=2)

    @mcp.resource("config://version", title="Version Information")
    def version_info() -> str:
        """Get version and build information."""
        version_data = {
            "version": settings.version,
            "app_name": settings.app_name,
            "mcp_sdk_version": "1.10.1",
            "python_version": "3.10+",
            "transport_protocol": settings.transport,
            "build_timestamp": datetime.now().isoformat()
        }
        return json.dumps(version_data, indent=2)

    @mcp.resource("config://capabilities", title="Server Capabilities")
    def server_capabilities() -> str:
        """Get server capabilities and features."""
        capabilities = {
            "mcp_version": "1.10.1",
            "transport": settings.transport,
            "features": {
                "tools": True,
                "resources": True,
                "prompts": True,
                "logging": True,
                "streaming": settings.transport in ["streamable-http", "sse"],
                "stateless": settings.stateless_http
            },
            "tools_count": 0,  # This would be dynamically calculated
            "resources_count": 0,  # This would be dynamically calculated
            "prompts_count": 0,  # This would be dynamically calculated
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(capabilities, indent=2)

    @mcp.resource("config://user/{user_id}", title="User Configuration")
    def user_config(user_id: str) -> str:
        """
        Get user-specific configuration.
        
        Args:
            user_id: The user identifier
        """
        # This is a template resource that demonstrates dynamic parameters
        user_data = {
            "user_id": user_id,
            "preferences": {
                "theme": "default",
                "language": "en",
                "timezone": "UTC"
            },
            "permissions": {
                "read": True,
                "write": False,
                "admin": False
            },
            "last_accessed": datetime.now().isoformat(),
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(user_data, indent=2)

    @mcp.resource("config://environment", title="Environment Variables")
    def environment_config() -> str:
        """Get environment-specific configuration (sanitized)."""
        env_data = {
            "environment": settings.environment,
            "debug_mode": settings.debug,
            "log_level": settings.log_level,
            "has_secret_key": settings.secret_key is not None,
            "has_api_key": settings.api_key is not None,
            "has_database_url": settings.database_url is not None,
            "has_redis_url": settings.redis_url is not None,
            "has_openai_api_key": settings.openai_api_key is not None,
            "has_anthropic_api_key": settings.anthropic_api_key is not None,
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(env_data, indent=2)
