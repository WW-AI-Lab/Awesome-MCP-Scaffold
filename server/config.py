"""
配置管理模块

使用 Pydantic Settings 进行环境变量管理和配置验证。
支持开发、测试、生产环境的不同配置。
"""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置设置"""

    # 基础配置
    app_name: str = Field(default="Awesome MCP Server", description="应用名称")
    version: str = Field(default="1.0.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    environment: Literal["development", "testing", "production"] = Field(
        default="development", description="运行环境"
    )

    # 服务器配置
    host: str = Field(default="127.0.0.1", description="服务器主机")
    port: int = Field(default=8000, description="服务器端口")
    transport: Literal["stdio", "streamable-http", "sse"] = Field(
        default="streamable-http", description="传输协议"
    )

    # MCP 配置
    mcp_mount_path: str = Field(default="/mcp", description="MCP 挂载路径")
    stateless_http: bool = Field(default=True, description="无状态 HTTP 模式")

    # 日志配置
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="日志级别"
    )
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="日志格式"
    )

    # 安全配置
    secret_key: str | None = Field(default=None, description="应用密钥")
    api_key: str | None = Field(default=None, description="API 密钥")

    # 数据库配置（可选）
    database_url: str | None = Field(default=None, description="数据库连接URL")

    # Redis 配置（可选）
    redis_url: str | None = Field(default=None, description="Redis 连接URL")

    # 外部服务配置
    openai_api_key: str | None = Field(default=None, description="OpenAI API 密钥")
    anthropic_api_key: str | None = Field(default=None, description="Anthropic API 密钥")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


# 全局设置实例 - 延迟初始化
settings = None


def get_settings() -> Settings:
    """获取设置实例"""
    global settings
    if settings is None:
        settings = Settings()
    return settings


# 初始化设置
settings = get_settings()





def is_development() -> bool:
    """检查是否为开发环境"""
    return settings.environment == "development"


def is_production() -> bool:
    """检查是否为生产环境"""
    return settings.environment == "production"


def is_testing() -> bool:
    """检查是否为测试环境"""
    return settings.environment == "testing"
