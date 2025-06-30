"""
系统信息资源模块

提供系统相关信息的 MCP 资源。
"""

import json
import platform
from datetime import datetime

import psutil
from mcp.server.fastmcp import FastMCP


def register_system_resources(mcp: FastMCP) -> None:
    """注册系统信息相关的资源"""

    @mcp.resource("system://info", title="System Information")
    def system_info() -> str:
        """Get basic system information."""
        info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(info, indent=2)

    @mcp.resource("system://memory", title="Memory Usage")
    def memory_usage() -> str:
        """Get current memory usage information."""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        info = {
            "virtual_memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percentage": memory.percent
            },
            "swap_memory": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percentage": swap.percent
            },
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(info, indent=2)

    @mcp.resource("system://cpu", title="CPU Information")
    def cpu_info() -> str:
        """Get CPU information and usage."""
        info = {
            "cpu_count": psutil.cpu_count(),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_freq": {
                "current": psutil.cpu_freq().current if psutil.cpu_freq() else None,
                "min": psutil.cpu_freq().min if psutil.cpu_freq() else None,
                "max": psutil.cpu_freq().max if psutil.cpu_freq() else None,
            },
            "load_average": list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else None,
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(info, indent=2)

    @mcp.resource("system://disk", title="Disk Usage")
    def disk_usage() -> str:
        """Get disk usage information."""
        disk = psutil.disk_usage('/')

        info = {
            "disk_usage": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percentage": (disk.used / disk.total) * 100
            },
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(info, indent=2)

    @mcp.resource("system://processes", title="Running Processes")
    def running_processes() -> str:
        """Get information about running processes."""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by CPU usage and take top 10
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        top_processes = processes[:10]

        info = {
            "total_processes": len(processes),
            "top_processes": top_processes,
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(info, indent=2)

    @mcp.resource("system://network", title="Network Information")
    def network_info() -> str:
        """Get network interface information."""
        interfaces = {}

        for interface, addrs in psutil.net_if_addrs().items():
            interfaces[interface] = []
            for addr in addrs:
                interfaces[interface].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })

        # Get network I/O statistics
        net_io = psutil.net_io_counters()

        info = {
            "interfaces": interfaces,
            "io_counters": {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            },
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(info, indent=2)
