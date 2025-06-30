# 📋 开发规范指南

> **面向 MCP 服务器脚手架的开发规范 - 确保代码质量和项目一致性**

## 🎯 规范概览

本文档定义了 **Awesome-MCP-Scaffold** 项目的开发规范，确保代码质量、可维护性和团队协作效率。作为脚手架项目，这些规范将成为基于此模板开发的 MCP 服务器的标准。

## 📁 项目结构规范

### 核心目录结构

```
awesome-mcp-scaffold/
├── server/                     # 🎯 MCP 服务器核心代码
│   ├── __init__.py            # 包初始化
│   ├── main.py                # FastMCP 主实例和应用入口
│   ├── config.py              # Pydantic Settings 配置管理
│   ├── tools/                 # MCP Tools 实现
│   │   ├── __init__.py        # 工具注册逻辑
│   │   ├── calculator.py      # 计算器工具示例
│   │   ├── text_processing.py # 文本处理工具示例
│   │   └── file_operations.py # 文件操作工具示例
│   ├── resources/             # MCP Resources 实现
│   │   ├── __init__.py        # 资源注册逻辑
│   │   ├── system_info.py     # 系统信息资源
│   │   └── config_data.py     # 配置数据资源
│   ├── prompts/               # MCP Prompts 实现
│   │   ├── __init__.py        # 提示注册逻辑
│   │   ├── code_review.py     # 代码审查提示
│   │   └── data_analysis.py   # 数据分析提示
│   └── routes/                # 旁路 REST API
│       ├── __init__.py        # 路由注册逻辑
│       └── api_routes.py      # 自定义 API 端点
├── tests/                     # 🧪 测试代码
│   ├── test_tools.py          # 工具测试
│   ├── test_resources.py      # 资源测试
│   ├── test_prompts.py        # 提示测试
│   └── conftest.py            # 测试配置
├── docs/                      # 📚 文档
├── deploy/                    # 🚀 部署配置
└── .cursor/rules/            # 🤖 Cursor AI 规则
```

### 文件命名规范

| 类型 | 命名规范 | 示例 |
|------|----------|------|
| **模块文件** | `snake_case.py` | `text_processing.py` |
| **类名** | `PascalCase` | `TextProcessor`, `WeatherAPI` |
| **函数名** | `snake_case` | `calculate_bmi`, `extract_emails` |
| **常量** | `UPPER_SNAKE_CASE` | `MAX_FILE_SIZE`, `DEFAULT_TIMEOUT` |
| **私有成员** | `_snake_case` | `_internal_helper`, `_cache_data` |

## 🛠️ MCP 组件开发规范

### 1. Tools (工具) 开发规范

#### 基本结构

```python
"""
工具模块文档字符串
描述工具的用途和功能
"""

from typing import Dict, Any
import logging
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

def register_tools(mcp: FastMCP) -> None:
    """注册所有工具到 MCP 实例"""
    
    @mcp.tool(
        title="工具标题",
        description="详细的工具描述，说明功能和用途"
    )
    def tool_name(param1: str, param2: int = 10) -> Dict[str, Any]:
        """
        工具的详细文档字符串
        
        Args:
            param1: 参数1的描述
            param2: 参数2的描述，默认值为10
            
        Returns:
            Dict[str, Any]: 返回结果的描述
            
        Raises:
            ValueError: 当输入无效时抛出
            RuntimeError: 当操作失败时抛出
        """
        logger.info(f"执行工具: {tool_name.__name__}", extra={
            "tool": tool_name.__name__,
            "param1": param1,
            "param2": param2
        })
        
        try:
            # 输入验证
            if not param1:
                raise ValueError("param1 不能为空")
            
            # 核心逻辑
            result = perform_operation(param1, param2)
            
            logger.info(f"工具执行成功: {tool_name.__name__}")
            return {
                "success": True,
                "result": result,
                "metadata": {
                    "tool": tool_name.__name__,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"工具执行失败: {tool_name.__name__}", exc_info=True)
            raise RuntimeError(f"工具执行失败: {str(e)}")

def perform_operation(param1: str, param2: int) -> Any:
    """辅助函数：执行具体操作"""
    # 实现具体逻辑
    pass
```

#### 工具开发最佳实践

1. **类型安全**
   ```python
   # ✅ 正确：使用完整的类型注解
   def calculate_bmi(weight_kg: float, height_m: float) -> Dict[str, float]:
       return {"bmi": weight_kg / (height_m ** 2)}
   
   # ❌ 错误：缺少类型注解
   def calculate_bmi(weight_kg, height_m):
       return {"bmi": weight_kg / (height_m ** 2)}
   ```

2. **输入验证**
   ```python
   # ✅ 正确：完整的输入验证
   def process_text(text: str, max_length: int = 1000) -> str:
       if not isinstance(text, str):
           raise TypeError("text 必须是字符串类型")
       if len(text) > max_length:
           raise ValueError(f"文本长度不能超过 {max_length} 字符")
       if not text.strip():
           raise ValueError("文本不能为空")
       return text.strip()
   ```

3. **错误处理**
   ```python
   # ✅ 正确：分层错误处理
   @mcp.tool()
   def api_call_tool(endpoint: str) -> Dict[str, Any]:
       try:
           response = httpx.get(endpoint, timeout=30)
           response.raise_for_status()
           return response.json()
       except httpx.TimeoutException:
           raise RuntimeError("API 调用超时")
       except httpx.HTTPStatusError as e:
           raise RuntimeError(f"API 返回错误状态: {e.response.status_code}")
       except Exception as e:
           logger.error("API 调用失败", exc_info=True)
           raise RuntimeError(f"API 调用失败: {str(e)}")
   ```

### 2. Resources (资源) 开发规范

#### 基本结构

```python
"""
资源模块文档字符串
"""

from mcp.server.fastmcp import FastMCP
import logging

logger = logging.getLogger(__name__)

def register_resources(mcp: FastMCP) -> None:
    """注册所有资源到 MCP 实例"""
    
    @mcp.resource(
        "scheme://{param}",
        title="资源标题",
        description="资源描述"
    )
    def resource_handler(param: str) -> str:
        """
        资源处理函数
        
        Args:
            param: 资源参数
            
        Returns:
            str: 资源内容
        """
        logger.info(f"获取资源: {param}")
        
        # 资源获取逻辑
        content = fetch_resource_content(param)
        
        return content

def fetch_resource_content(param: str) -> str:
    """获取资源内容的辅助函数"""
    # 实现具体逻辑
    pass
```

### 3. Prompts (提示) 开发规范

#### 基本结构

```python
"""
提示模块文档字符串
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

def register_prompts(mcp: FastMCP) -> None:
    """注册所有提示到 MCP 实例"""
    
    @mcp.prompt(
        title="提示标题",
        description="提示描述"
    )
    def prompt_template(context: Dict[str, Any]) -> str:
        """
        提示模板函数
        
        Args:
            context: 上下文数据
            
        Returns:
            str: 生成的提示内容
        """
        # 验证必需的上下文参数
        required_keys = ["key1", "key2"]
        for key in required_keys:
            if key not in context:
                raise ValueError(f"缺少必需的上下文参数: {key}")
        
        # 生成提示内容
        prompt = f"""
        基于以下信息生成提示:
        
        参数1: {context['key1']}
        参数2: {context['key2']}
        
        请提供详细的分析和建议。
        """
        
        return prompt.strip()
```

## 🧪 测试开发规范

### 测试文件结构

```python
"""
测试模块文档字符串
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path


class TestToolName:
    """工具测试类"""
    
    def test_normal_case(self):
        """测试正常情况"""
        # Arrange
        input_data = "test_input"
        expected = "expected_output"
        
        # Act
        result = tool_function(input_data)
        
        # Assert
        assert result == expected
    
    def test_edge_case(self):
        """测试边界情况"""
        pass
    
    def test_error_handling(self):
        """测试错误处理"""
        with pytest.raises(ValueError, match="错误信息模式"):
            tool_function("invalid_input")
    
    @pytest.mark.asyncio
    async def test_async_operation(self):
        """测试异步操作"""
        result = await async_tool_function("input")
        assert result is not None


@pytest.fixture
def sample_data():
    """测试数据 fixture"""
    return {
        "key": "value",
        "number": 123
    }


@pytest.fixture
def temp_file():
    """临时文件 fixture"""
    test_file = Path("test_temp.txt")
    test_file.write_text("test content")
    
    yield test_file
    
    # 清理
    test_file.unlink(missing_ok=True)
```

### 测试命名规范

| 测试类型 | 命名模式 | 示例 |
|----------|----------|------|
| **单元测试** | `test_<function_name>_<scenario>` | `test_calculate_bmi_normal_input` |
| **集成测试** | `test_<component>_integration` | `test_mcp_server_integration` |
| **错误测试** | `test_<function_name>_<error_type>` | `test_divide_zero_error` |

## 📝 代码质量规范

### 1. 文档字符串规范

```python
def complex_function(param1: str, param2: int, param3: bool = False) -> Dict[str, Any]:
    """
    函数的简短描述（一行）
    
    更详细的函数描述，可以多行。
    说明函数的用途、算法、注意事项等。
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
        param3: 参数3的描述，默认为 False
    
    Returns:
        Dict[str, Any]: 返回字典，包含以下键：
            - "result": 处理结果
            - "status": 状态信息
            - "metadata": 元数据
    
    Raises:
        ValueError: 当 param1 为空时
        TypeError: 当参数类型不正确时
        RuntimeError: 当处理失败时
    
    Example:
        >>> result = complex_function("test", 42, True)
        >>> print(result["status"])
        "success"
    
    Note:
        这是一个重要的注意事项
    """
    pass
```

### 2. 日志规范

```python
import logging
import structlog

# 使用结构化日志
logger = structlog.get_logger()

def example_function(param: str) -> str:
    """示例函数"""
    logger.info(
        "函数开始执行",
        function="example_function",
        param=param,
        user_id=get_current_user_id()
    )
    
    try:
        result = process_param(param)
        
        logger.info(
            "函数执行成功",
            function="example_function",
            result_length=len(result)
        )
        
        return result
        
    except Exception as e:
        logger.error(
            "函数执行失败",
            function="example_function",
            error=str(e),
            param=param,
            exc_info=True
        )
        raise
```

### 3. 配置管理规范

```python
# config.py
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置"""
    
    # 分组配置，使用注释分隔
    # === 基础配置 ===
    app_name: str = Field(default="MCP Server", description="应用名称")
    version: str = Field(default="1.0.0", description="版本号")
    
    # === 服务器配置 ===
    host: str = Field(default="127.0.0.1", description="服务器地址")
    port: int = Field(default=8000, ge=1, le=65535, description="服务器端口")
    
    # === 安全配置 ===
    secret_key: str | None = Field(default=None, description="应用密钥")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }

# 使用配置
from server.config import settings

def use_config():
    """使用配置的示例"""
    if settings.debug:
        logger.setLevel(logging.DEBUG)
```

## 🔧 开发工具配置

### 1. 代码格式化 (Ruff)

```toml
# pyproject.toml
[tool.ruff]
target-version = "py310"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings  
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501", # line too long
    "B008", # function calls in argument defaults
]
```

### 2. 类型检查 (MyPy)

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.10"
check_untyped_defs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
```

### 3. 测试配置 (Pytest)

```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "slow: 标记慢速测试",
    "integration: 标记集成测试",
    "unit: 标记单元测试",
]
```

## 🚀 开发工作流

### 1. 功能开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/new-tool

# 2. 开发功能
# 编写代码 -> 编写测试 -> 运行测试

# 3. 代码检查
make lint
make format

# 4. 运行测试
make test

# 5. 提交代码
git add .
git commit -m "feat: add new calculation tool"

# 6. 推送分支
git push origin feature/new-tool

# 7. 创建 Pull Request
```

### 2. 日常开发命令

```bash
# 安装依赖
make install

# 启动开发服务器
make dev

# 运行测试
make test

# 代码检查
make lint

# 代码格式化
make format

# 生成测试覆盖率报告
make coverage
```

### 3. Git 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**提交类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建工具或辅助工具的变动

**示例：**
```bash
git commit -m "feat(tools): add weather query tool with city and coordinates support"
git commit -m "fix(resources): resolve memory leak in system info resource"
git commit -m "docs(readme): update installation instructions"
```

## 📊 性能和监控规范

### 1. 性能监控

```python
import time
from functools import wraps

def monitor_performance(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(
                "函数执行完成",
                function=func.__name__,
                duration=duration,
                success=True
            )
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error(
                "函数执行失败",
                function=func.__name__,
                duration=duration,
                error=str(e),
                success=False
            )
            raise
    
    return wrapper

@monitor_performance
@mcp.tool()
def monitored_tool(param: str) -> str:
    """被监控的工具"""
    return process_data(param)
```

### 2. 缓存策略

```python
from functools import lru_cache
from typing import Dict, Any

@lru_cache(maxsize=128)
def expensive_computation(param: str) -> str:
    """昂贵的计算操作，使用 LRU 缓存"""
    # 执行昂贵的计算
    return result

# 使用 TTL 缓存
import time
from typing import Optional

class TTLCache:
    """简单的 TTL 缓存实现"""
    
    def __init__(self, ttl: int = 300):
        self.cache: Dict[str, tuple] = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        self.cache[key] = (value, time.time())

# 全局缓存实例
cache = TTLCache(ttl=300)  # 5分钟 TTL
```

## 🔒 安全开发规范

### 1. 输入验证

```python
import re
from pathlib import Path

def validate_file_path(file_path: str, base_dir: Path) -> Path:
    """验证文件路径安全性"""
    # 规范化路径
    normalized_path = Path(file_path).resolve()
    
    # 检查是否在允许的目录内
    if not normalized_path.is_relative_to(base_dir):
        raise ValueError(f"文件路径不在允许的目录内: {file_path}")
    
    return normalized_path

def validate_email(email: str) -> str:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError(f"无效的邮箱格式: {email}")
    return email

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """清理用户输入"""
    # 移除危险字符
    sanitized = re.sub(r'[<>"\'\&]', '', text)
    
    # 限制长度
    if len(sanitized) > max_length:
        raise ValueError(f"输入长度不能超过 {max_length} 字符")
    
    return sanitized.strip()
```

### 2. 敏感信息处理

```python
import os
from typing import Optional

def get_api_key(service: str) -> str:
    """安全地获取 API 密钥"""
    key = os.getenv(f"{service.upper()}_API_KEY")
    if not key:
        raise ValueError(f"未找到 {service} API 密钥")
    return key

def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """遮蔽敏感数据"""
    if len(data) <= visible_chars:
        return "*" * len(data)
    
    return data[:visible_chars] + "*" * (len(data) - visible_chars)

# 日志中遮蔽敏感信息
def log_request(endpoint: str, api_key: str) -> None:
    """记录请求日志，遮蔽敏感信息"""
    logger.info(
        "API 请求",
        endpoint=endpoint,
        api_key=mask_sensitive_data(api_key)
    )
```

## 📋 代码审查清单

### Pull Request 检查清单

- [ ] **功能完整性**
  - [ ] 功能按需求实现
  - [ ] 边界条件处理
  - [ ] 错误处理完善

- [ ] **代码质量**
  - [ ] 遵循命名规范
  - [ ] 类型注解完整
  - [ ] 文档字符串清晰
  - [ ] 无重复代码

- [ ] **测试覆盖**
  - [ ] 单元测试覆盖主要功能
  - [ ] 边界条件测试
  - [ ] 错误处理测试
  - [ ] 测试通过率 100%

- [ ] **性能和安全**
  - [ ] 无明显性能问题
  - [ ] 输入验证充分
  - [ ] 敏感信息处理安全
  - [ ] 资源使用合理

- [ ] **文档更新**
  - [ ] README 更新（如需要）
  - [ ] API 文档更新（如需要）
  - [ ] 变更日志记录

## 🎯 最佳实践总结

### 开发原则

1. **KISS 原则**：保持简单和直接
2. **DRY 原则**：不要重复代码
3. **SOLID 原则**：面向对象设计原则
4. **测试驱动**：先写测试，再写实现
5. **文档先行**：代码即文档

### 质量保证

1. **自动化测试**：确保功能正确性
2. **代码审查**：提高代码质量
3. **持续集成**：自动化构建和测试
4. **性能监控**：及时发现性能问题
5. **安全审计**：定期安全检查