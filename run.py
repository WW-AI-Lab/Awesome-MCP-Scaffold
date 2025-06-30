#!/usr/bin/env python3
"""
Awesome MCP Scaffold 启动脚本

简化的启动入口，支持多种运行模式。
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from server.main import main


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="Awesome MCP Scaffold - 启动 MCP 服务器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python run.py                          # 使用默认配置启动
  python run.py --transport stdio        # 使用 stdio 传输
  python run.py --port 9000              # 指定端口
  python run.py --debug                  # 启用调试模式
  python run.py --env production         # 生产环境模式
        """
    )
    
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="streamable-http",
        help="传输协议 (默认: streamable-http)"
    )
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="服务器主机地址 (默认: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服务器端口 (默认: 8000)"
    )
    
    parser.add_argument(
        "--env",
        choices=["development", "testing", "production"],
        default="development",
        help="运行环境 (默认: development)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="日志级别 (默认: INFO)"
    )
    
    return parser


def main_cli():
    """命令行主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 设置环境变量
    import os
    os.environ["TRANSPORT"] = args.transport
    os.environ["HOST"] = args.host
    os.environ["PORT"] = str(args.port)
    os.environ["ENVIRONMENT"] = args.env
    os.environ["DEBUG"] = str(args.debug).lower()
    os.environ["LOG_LEVEL"] = args.log_level
    
    # 显示启动信息
    print("🚀 Awesome MCP Scaffold")
    print("=" * 50)
    print(f"📡 传输协议: {args.transport}")
    print(f"🏠 主机地址: {args.host}")
    print(f"🔌 端口号: {args.port}")
    print(f"🌍 运行环境: {args.env}")
    print(f"🐛 调试模式: {'开启' if args.debug else '关闭'}")
    print(f"📝 日志级别: {args.log_level}")
    print("=" * 50)
    
    if args.transport == "streamable-http":
        print(f"🌐 访问地址: http://{args.host}:{args.port}")
        print(f"🔍 健康检查: http://{args.host}:{args.port}/health")
        print(f"📊 服务器信息: http://{args.host}:{args.port}/info")
        print(f"🔧 MCP 端点: http://{args.host}:{args.port}/mcp")
        print("=" * 50)
    
    # 启动服务器
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main_cli() 