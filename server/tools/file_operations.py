"""
文件操作工具模块

提供安全的文件读取和操作功能的 MCP 工具。
注意：为了安全考虑，这些工具只允许访问特定目录。
"""

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP


def register_file_tools(mcp: FastMCP) -> None:
    """注册文件操作相关的工具"""

    # 定义安全的工作目录
    SAFE_DIR = Path.cwd() / "workspace"
    SAFE_DIR.mkdir(exist_ok=True)

    def _get_safe_path(file_path: str) -> Path:
        """获取安全的文件路径，确保在允许的目录内"""
        path = SAFE_DIR / file_path
        # 确保路径在安全目录内
        try:
            path.resolve().relative_to(SAFE_DIR.resolve())
            return path
        except ValueError:
            raise ValueError(f"Access denied: Path {file_path} is outside safe directory")

    @mcp.tool(title="List Directory", description="List files and directories")
    def list_directory(directory_path: str = ".") -> dict[str, list[str]]:
        """
        List files and directories in the specified path.
        
        Args:
            directory_path: Relative path within the workspace directory
        """
        safe_path = _get_safe_path(directory_path)

        if not safe_path.exists():
            raise FileNotFoundError(f"Directory {directory_path} not found")

        if not safe_path.is_dir():
            raise ValueError(f"{directory_path} is not a directory")

        files = []
        directories = []

        for item in safe_path.iterdir():
            if item.is_file():
                files.append(item.name)
            elif item.is_dir():
                directories.append(item.name)

        return {
            "files": sorted(files),
            "directories": sorted(directories),
            "path": directory_path
        }

    @mcp.tool(title="Read Text File", description="Read content of a text file")
    def read_text_file(file_path: str) -> dict[str, str]:
        """
        Read the content of a text file.
        
        Args:
            file_path: Relative path to the file within workspace
        """
        safe_path = _get_safe_path(file_path)

        if not safe_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")

        if not safe_path.is_file():
            raise ValueError(f"{file_path} is not a file")

        try:
            content = safe_path.read_text(encoding='utf-8')
            return {
                "content": content,
                "file_path": file_path,
                "size_bytes": safe_path.stat().st_size,
                "lines": len(content.split('\n'))
            }
        except UnicodeDecodeError:
            raise ValueError(f"File {file_path} is not a valid text file")

    @mcp.tool(title="Write Text File", description="Write content to a text file")
    def write_text_file(file_path: str, content: str, overwrite: bool = False) -> dict[str, str]:
        """
        Write content to a text file.
        
        Args:
            file_path: Relative path to the file within workspace
            content: Content to write
            overwrite: Whether to overwrite existing file
        """
        safe_path = _get_safe_path(file_path)

        if safe_path.exists() and not overwrite:
            raise ValueError(f"File {file_path} already exists. Set overwrite=True to replace it.")

        # Create parent directories if they don't exist
        safe_path.parent.mkdir(parents=True, exist_ok=True)

        safe_path.write_text(content, encoding='utf-8')

        return {
            "message": f"Successfully wrote to {file_path}",
            "file_path": file_path,
            "size_bytes": safe_path.stat().st_size,
            "lines": len(content.split('\n'))
        }

    @mcp.tool(title="Read JSON File", description="Read and parse a JSON file")
    def read_json_file(file_path: str) -> dict:
        """
        Read and parse a JSON file.
        
        Args:
            file_path: Relative path to the JSON file within workspace
        """
        safe_path = _get_safe_path(file_path)

        if not safe_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")

        try:
            with safe_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            return {
                "data": data,
                "file_path": file_path,
                "size_bytes": safe_path.stat().st_size
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}")

    @mcp.tool(title="Write JSON File", description="Write data to a JSON file")
    def write_json_file(file_path: str, data: dict, overwrite: bool = False, indent: int = 2) -> dict[str, str]:
        """
        Write data to a JSON file.
        
        Args:
            file_path: Relative path to the file within workspace
            data: Data to write as JSON
            overwrite: Whether to overwrite existing file
            indent: JSON indentation level
        """
        safe_path = _get_safe_path(file_path)

        if safe_path.exists() and not overwrite:
            raise ValueError(f"File {file_path} already exists. Set overwrite=True to replace it.")

        # Create parent directories if they don't exist
        safe_path.parent.mkdir(parents=True, exist_ok=True)

        with safe_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

        return {
            "message": f"Successfully wrote JSON to {file_path}",
            "file_path": file_path,
            "size_bytes": safe_path.stat().st_size
        }

    @mcp.tool(title="File Info", description="Get file information")
    def file_info(file_path: str) -> dict:
        """
        Get detailed information about a file or directory.
        
        Args:
            file_path: Relative path to the file within workspace
        """
        safe_path = _get_safe_path(file_path)

        if not safe_path.exists():
            raise FileNotFoundError(f"Path {file_path} not found")

        stat = safe_path.stat()

        return {
            "path": file_path,
            "name": safe_path.name,
            "type": "file" if safe_path.is_file() else "directory",
            "size_bytes": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "exists": True
        }

    @mcp.tool(title="Create Directory", description="Create a new directory")
    def create_directory(directory_path: str) -> dict[str, str]:
        """
        Create a new directory.
        
        Args:
            directory_path: Relative path for the new directory
        """
        safe_path = _get_safe_path(directory_path)

        safe_path.mkdir(parents=True, exist_ok=True)

        return {
            "message": f"Directory {directory_path} created successfully",
            "path": directory_path
        }
