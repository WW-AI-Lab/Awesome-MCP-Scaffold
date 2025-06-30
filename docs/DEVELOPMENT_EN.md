# 📋 Development Standards Guide

> **Development Standards for MCP Server Scaffold - Ensuring Code Quality and Project Consistency**

## 🎯 Standards Overview

This document defines the development standards for the **Awesome-MCP-Scaffold** project, ensuring code quality, maintainability, and team collaboration efficiency. As a scaffold project, these standards will become the benchmark for MCP servers developed based on this template.

## 📁 Project Structure Standards

### Core Directory Structure

```
awesome-mcp-scaffold/
├── server/                     # 🎯 MCP server core code
│   ├── __init__.py            # Package initialization
│   ├── main.py                # FastMCP main instance and app entry
│   ├── config.py              # Pydantic Settings configuration management
│   ├── tools/                 # MCP Tools implementation
│   │   ├── __init__.py        # Tool registration logic
│   │   ├── calculator.py      # Calculator tool example
│   │   ├── text_processing.py # Text processing tool example
│   │   └── file_operations.py # File operation tool example
│   ├── resources/             # MCP Resources implementation
│   │   ├── __init__.py        # Resource registration logic
│   │   ├── system_info.py     # System information resource
│   │   └── config_data.py     # Configuration data resource
│   ├── prompts/               # MCP Prompts implementation
│   │   ├── __init__.py        # Prompt registration logic
│   │   ├── code_review.py     # Code review prompt
│   │   └── data_analysis.py   # Data analysis prompt
│   └── routes/                # Bypass REST API
│       ├── __init__.py        # Route registration logic
│       └── api_routes.py      # Custom API endpoints
├── tests/                     # 🧪 Test code
│   ├── test_tools.py          # Tool tests
│   ├── test_resources.py      # Resource tests
│   ├── test_prompts.py        # Prompt tests
│   └── conftest.py            # Test configuration
├── docs/                      # 📚 Documentation
├── deploy/                    # 🚀 Deployment configuration
└── .cursor/rules/            # 🤖 Cursor AI rules
```

### File Naming Standards

| Type | Naming Convention | Example |
|------|-------------------|---------|
| **Module files** | `snake_case.py` | `text_processing.py` |
| **Class names** | `PascalCase` | `TextProcessor`, `WeatherAPI` |
| **Function names** | `snake_case` | `calculate_bmi`, `extract_emails` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_FILE_SIZE`, `DEFAULT_TIMEOUT` |
| **Private members** | `_snake_case` | `_internal_helper`, `_cache_data` |

## 🛠️ MCP Component Development Standards

### 1. Tools Development Standards

#### Basic Structure

```python
"""
Tool module docstring
Describe the purpose and functionality of the tool
"""

from typing import Dict, Any
import logging
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

def register_tools(mcp: FastMCP) -> None:
    """Register all tools to MCP instance"""
    
    @mcp.tool(
        title="Tool Title",
        description="Detailed tool description explaining functionality and purpose"
    )
    def tool_name(param1: str, param2: int = 10) -> Dict[str, Any]:
        """
        Detailed docstring for the tool
        
        Args:
            param1: Description of parameter 1
            param2: Description of parameter 2, default value is 10
            
        Returns:
            Dict[str, Any]: Description of return result
            
        Raises:
            ValueError: Raised when input is invalid
            RuntimeError: Raised when operation fails
        """
        logger.info(f"Executing tool: {tool_name.__name__}", extra={
            "tool": tool_name.__name__,
            "param1": param1,
            "param2": param2
        })
        
        try:
            # Input validation
            if not param1:
                raise ValueError("param1 cannot be empty")
            
            # Core logic
            result = perform_operation(param1, param2)
            
            logger.info(f"Tool execution successful: {tool_name.__name__}")
            return {
                "success": True,
                "result": result,
                "metadata": {
                    "tool": tool_name.__name__,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Tool execution failed: {tool_name.__name__}", exc_info=True)
            raise RuntimeError(f"Tool execution failed: {str(e)}")

def perform_operation(param1: str, param2: int) -> Any:
    """Helper function: perform specific operation"""
    # Implement specific logic
    pass
```

#### Tool Development Best Practices

1. **Type Safety**
   ```python
   # ✅ Correct: Use complete type annotations
   def calculate_bmi(weight_kg: float, height_m: float) -> Dict[str, float]:
       return {"bmi": weight_kg / (height_m ** 2)}
   
   # ❌ Wrong: Missing type annotations
   def calculate_bmi(weight_kg, height_m):
       return {"bmi": weight_kg / (height_m ** 2)}
   ```

2. **Input Validation**
   ```python
   # ✅ Correct: Complete input validation
   def process_text(text: str, max_length: int = 1000) -> str:
       if not isinstance(text, str):
           raise TypeError("text must be string type")
       if len(text) > max_length:
           raise ValueError(f"text length cannot exceed {max_length} characters")
       if not text.strip():
           raise ValueError("text cannot be empty")
       return text.strip()
   ```

3. **Error Handling**
   ```python
   # ✅ Correct: Layered error handling
   @mcp.tool()
   def api_call_tool(endpoint: str) -> Dict[str, Any]:
       try:
           response = httpx.get(endpoint, timeout=30)
           response.raise_for_status()
           return response.json()
       except httpx.TimeoutException:
           raise RuntimeError("API call timeout")
       except httpx.HTTPStatusError as e:
           raise RuntimeError(f"API returned error status: {e.response.status_code}")
       except Exception as e:
           logger.error("API call failed", exc_info=True)
           raise RuntimeError(f"API call failed: {str(e)}")
   ```

### 2. Resources Development Standards

#### Basic Structure

```python
"""
Resource module docstring
"""

from mcp.server.fastmcp import FastMCP
import logging

logger = logging.getLogger(__name__)

def register_resources(mcp: FastMCP) -> None:
    """Register all resources to MCP instance"""
    
    @mcp.resource(
        "scheme://{param}",
        title="Resource Title",
        description="Resource Description"
    )
    def resource_handler(param: str) -> str:
        """
        Resource handler function
        
        Args:
            param: Resource parameter
        """
        # Implement resource handler logic
        pass 