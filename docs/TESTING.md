# 🧪 测试指南

> **MCP 服务器脚手架的全面测试策略 - 确保代码质量和功能可靠性**

## 🎯 测试策略概览

本文档提供 **Awesome-MCP-Scaffold** 项目的完整测试指南，涵盖 MCP 协议的特殊测试需求和最佳实践。作为脚手架项目，这些测试模式将指导基于此模板开发的 MCP 服务器。

## 📊 测试层次架构

### 测试金字塔

```
    🔺 E2E 测试 (5%)
       ├── MCP 客户端集成测试
       └── 完整工作流验证
    
    🔷 集成测试 (25%)
       ├── HTTP API 端点测试
       ├── MCP 协议交互测试
       └── 数据库/外部服务集成
    
    🔶 单元测试 (70%)
       ├── Tools 功能测试
       ├── Resources 逻辑测试
       ├── Prompts 模板测试
       └── 工具函数测试
```

### 测试覆盖目标

| 组件类型 | 覆盖率目标 | 重点测试内容 |
|----------|-----------|-------------|
| **MCP Tools** | 95%+ | 功能正确性、输入验证、错误处理 |
| **MCP Resources** | 90%+ | 数据获取、缓存机制、权限控制 |
| **MCP Prompts** | 85%+ | 模板渲染、参数验证、输出格式 |
| **HTTP Routes** | 90%+ | 端点响应、状态码、数据格式 |
| **配置管理** | 80%+ | 环境变量、默认值、验证逻辑 |

## 🛠️ 测试环境配置

### 1. 测试依赖安装

```bash
# 安装测试相关依赖
pip install pytest pytest-asyncio pytest-cov pytest-mock httpx
pip install faker factory-boy freezegun

# 或使用项目配置
pip install -e ".[dev]"
```

### 2. pytest 配置

```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "-ra",
    "-q", 
    "--strict-markers",
    "--strict-config",
    "--cov=server",
    "--cov-report=html",
    "--cov-report=term-missing"
]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "unit: 单元测试",
    "integration: 集成测试", 
    "e2e: 端到端测试",
    "slow: 慢速测试",
    "external: 需要外部服务的测试"
]
```

### 3. 测试环境隔离

```python
# tests/conftest.py
"""
测试配置和 fixtures
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock

from server.config import Settings


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """设置测试环境变量"""
    # 创建临时测试目录
    test_dir = tempfile.mkdtemp()
    
    # 设置测试环境变量
    os.environ.update({
        "ENVIRONMENT": "testing",
        "LOG_LEVEL": "DEBUG",
        "TEST_DATA_DIR": test_dir,
        "DATABASE_URL": "sqlite:///test.db",
        "REDIS_URL": "redis://localhost:6379/1"
    })
    
    yield test_dir
    
    # 清理
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture
def test_settings():
    """测试配置 fixture"""
    return Settings(
        environment="testing",
        debug=True,
        log_level="DEBUG"
    )


@pytest.fixture
def workspace_dir():
    """工作目录 fixture"""
    workspace = Path.cwd() / "workspace"
    workspace.mkdir(exist_ok=True)
    
    yield workspace
    
    # 可选：清理测试文件
    # import shutil
    # shutil.rmtree(workspace, ignore_errors=True)


@pytest.fixture
def sample_json_data():
    """示例 JSON 数据"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30,
        "skills": ["Python", "MCP", "Testing"]
    }


@pytest.fixture
def mock_external_api():
    """模拟外部 API"""
    mock = Mock()
    mock.get.return_value.json.return_value = {"status": "success"}
    mock.get.return_value.status_code = 200
    return mock
```

## 🔧 MCP Tools 测试

### 1. 基本工具测试

```python
# tests/test_tools.py
"""
MCP 工具测试
"""

import pytest
from unittest.mock import patch, Mock
from server.tools.calculator import add, subtract, calculate_bmi
from server.tools.text_processing import count_words, extract_emails
from server.tools.file_operations import read_file, write_file


class TestCalculatorTools:
    """计算器工具测试"""

    def test_add_positive_numbers(self):
        """测试正数加法"""
        result = add(5, 3)
        assert result == 8

    def test_add_negative_numbers(self):
        """测试负数加法"""
        result = add(-5, -3)
        assert result == -8

    def test_add_mixed_numbers(self):
        """测试正负数混合加法"""
        result = add(5, -3)
        assert result == 2

    def test_add_zero(self):
        """测试零值加法"""
        result = add(0, 5)
        assert result == 5

    def test_add_float_precision(self):
        """测试浮点数精度"""
        result = add(0.1, 0.2)
        assert result == pytest.approx(0.3, rel=1e-9)

    def test_subtract_basic(self):
        """测试基本减法"""
        result = subtract(10, 3)
        assert result == 7

    def test_divide_by_zero(self):
        """测试除零错误"""
        from server.tools.calculator import divide
        
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_calculate_bmi_normal(self):
        """测试正常 BMI 计算"""
        # 70kg, 1.75m -> BMI ≈ 22.86
        result = calculate_bmi(70, 1.75)
        expected_bmi = 70 / (1.75 ** 2)
        
        assert result["bmi"] == pytest.approx(expected_bmi, rel=1e-2)
        assert result["category"] in ["正常体重", "Normal"]

    def test_calculate_bmi_invalid_weight(self):
        """测试无效体重"""
        with pytest.raises(ValueError, match="Weight must be positive"):
            calculate_bmi(-70, 1.75)

    def test_calculate_bmi_invalid_height(self):
        """测试无效身高"""
        with pytest.raises(ValueError, match="Height must be positive"):
            calculate_bmi(70, 0)

    @pytest.mark.parametrize("weight,height,expected_category", [
        (45, 1.70, "偏瘦"),
        (70, 1.75, "正常"),
        (90, 1.75, "偏胖"),
        (110, 1.75, "肥胖")
    ])
    def test_bmi_categories(self, weight, height, expected_category):
        """测试 BMI 分类"""
        result = calculate_bmi(weight, height)
        # 这里需要根据实际实现调整断言
        assert "category" in result


class TestTextProcessingTools:
    """文本处理工具测试"""

    def test_count_words_simple(self):
        """测试简单单词计数"""
        text = "Hello world this is a test"
        result = count_words(text)
        
        assert result["words"] == 6
        assert result["characters"] == 26
        assert result["lines"] == 1

    def test_count_words_empty(self):
        """测试空文本"""
        result = count_words("")
        
        assert result["words"] == 0
        assert result["characters"] == 0

    def test_count_words_multiline(self):
        """测试多行文本"""
        text = "Line 1\nLine 2\nLine 3"
        result = count_words(text)
        
        assert result["lines"] == 3
        assert result["words"] == 6

    def test_extract_emails_single(self):
        """测试提取单个邮箱"""
        text = "Contact us at test@example.com for more info"
        result = extract_emails(text)
        
        assert result == ["test@example.com"]

    def test_extract_emails_multiple(self):
        """测试提取多个邮箱"""
        text = "Email admin@test.org or support@company.com"
        result = extract_emails(text)
        
        assert len(result) == 2
        assert "admin@test.org" in result
        assert "support@company.com" in result

    def test_extract_emails_none(self):
        """测试无邮箱文本"""
        text = "This text has no email addresses"
        result = extract_emails(text)
        
        assert result == []

    def test_extract_emails_invalid(self):
        """测试无效邮箱格式"""
        text = "Invalid emails: test@, @example.com, test.com"
        result = extract_emails(text)
        
        assert result == []

    @pytest.mark.parametrize("input_text,expected_slug", [
        ("Hello World", "hello-world"),
        ("Test with 123 Numbers!", "test-with-123-numbers"),
        ("Special@#$%Characters", "special-characters"),
        ("Multiple   Spaces", "multiple-spaces")
    ])
    def test_text_to_slug(self, input_text, expected_slug):
        """测试文本转 slug"""
        from server.tools.text_processing import text_to_slug
        result = text_to_slug(input_text)
        assert result == expected_slug


class TestFileOperationTools:
    """文件操作工具测试"""

    def test_read_file_success(self, workspace_dir):
        """测试成功读取文件"""
        # 创建测试文件
        test_file = workspace_dir / "test.txt"
        test_content = "This is test content"
        test_file.write_text(test_content)
        
        # 测试读取
        result = read_file("test.txt")
        assert result == test_content

    def test_read_file_not_found(self):
        """测试文件不存在"""
        with pytest.raises(FileNotFoundError):
            read_file("nonexistent.txt")

    def test_read_file_path_traversal(self):
        """测试路径遍历攻击"""
        with pytest.raises(ValueError, match="Path is outside workspace"):
            read_file("../../../etc/passwd")

    def test_write_file_success(self, workspace_dir):
        """测试成功写入文件"""
        content = "New file content"
        result = write_file("new_file.txt", content)
        
        assert result["success"] is True
        
        # 验证文件内容
        written_file = workspace_dir / "new_file.txt"
        assert written_file.exists()
        assert written_file.read_text() == content

    def test_write_file_overwrite(self, workspace_dir):
        """测试覆盖现有文件"""
        filename = "overwrite_test.txt"
        original_content = "Original content"
        new_content = "New content"
        
        # 创建原始文件
        write_file(filename, original_content)
        
        # 覆盖文件
        result = write_file(filename, new_content)
        
        assert result["success"] is True
        
        # 验证内容已更新
        test_file = workspace_dir / filename
        assert test_file.read_text() == new_content

    def test_json_operations(self, workspace_dir, sample_json_data):
        """测试 JSON 文件操作"""
        from server.tools.file_operations import write_json_file, read_json_file
        
        filename = "test_data.json"
        
        # 写入 JSON
        write_result = write_json_file(filename, sample_json_data)
        assert write_result["success"] is True
        
        # 读取 JSON
        read_result = read_json_file(filename)
        assert read_result == sample_json_data

    def test_list_directory(self, workspace_dir):
        """测试目录列表"""
        from server.tools.file_operations import list_directory
        
        # 创建测试文件和目录
        (workspace_dir / "file1.txt").write_text("content1")
        (workspace_dir / "file2.txt").write_text("content2")
        (workspace_dir / "subdir").mkdir()
        
        result = list_directory(".")
        
        assert "file1.txt" in result["files"]
        assert "file2.txt" in result["files"]
        assert "subdir" in result["directories"]
```

### 2. 异步工具测试

```python
class TestAsyncTools:
    """异步工具测试"""

    @pytest.mark.asyncio
    async def test_async_api_call(self, mock_external_api):
        """测试异步 API 调用工具"""
        from server.tools.api_client import fetch_data
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value.json.return_value = {
                "data": "test response"
            }
            
            result = await fetch_data("https://api.example.com/data")
            
            assert result["data"] == "test response"

    @pytest.mark.asyncio
    async def test_async_timeout(self):
        """测试异步超时处理"""
        import asyncio
        from server.tools.api_client import fetch_data_with_timeout
        
        with patch('httpx.AsyncClient') as mock_client:
            # 模拟超时
            mock_client.return_value.__aenter__.return_value.get.side_effect = asyncio.TimeoutError()
            
            with pytest.raises(RuntimeError, match="Request timeout"):
                await fetch_data_with_timeout("https://slow-api.com", timeout=1)
```

## 📡 MCP Resources 测试

```python
# tests/test_resources.py
"""
MCP 资源测试
"""

import pytest
from unittest.mock import patch, Mock
from server.resources.system_info import get_system_info
from server.resources.config_data import get_config_data


class TestSystemInfoResource:
    """系统信息资源测试"""

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_get_cpu_memory_info(self, mock_memory, mock_cpu):
        """测试 CPU 和内存信息获取"""
        # 模拟系统数据
        mock_cpu.return_value = 45.5
        mock_memory.return_value = Mock(
            total=8589934592,  # 8GB
            available=4294967296,  # 4GB
            percent=50.0
        )
        
        result = get_system_info("cpu_memory")
        
        assert result["cpu_percent"] == 45.5
        assert result["memory_total"] == 8589934592
        assert result["memory_available"] == 4294967296
        assert result["memory_percent"] == 50.0

    @patch('psutil.disk_usage')
    def test_get_disk_info(self, mock_disk):
        """测试磁盘信息获取"""
        mock_disk.return_value = Mock(
            total=1000000000000,  # 1TB
            used=500000000000,    # 500GB
            free=500000000000     # 500GB
        )
        
        result = get_system_info("disk")
        
        assert result["disk_total"] == 1000000000000
        assert result["disk_used"] == 500000000000
        assert result["disk_free"] == 500000000000

    def test_get_invalid_resource(self):
        """测试无效资源请求"""
        with pytest.raises(ValueError, match="Unknown resource type"):
            get_system_info("invalid_resource")

    @patch('server.resources.system_info.cache')
    def test_resource_caching(self, mock_cache):
        """测试资源缓存机制"""
        # 模拟缓存命中
        cached_data = {"cpu_percent": 30.0, "cached": True}
        mock_cache.get.return_value = cached_data
        
        result = get_system_info("cpu_memory")
        
        assert result == cached_data
        mock_cache.get.assert_called_once()


class TestConfigDataResource:
    """配置数据资源测试"""

    def test_get_app_config(self, test_settings):
        """测试应用配置获取"""
        result = get_config_data("app_config")
        
        assert "app_name" in result
        assert "version" in result
        assert "environment" in result

    def test_get_user_config(self):
        """测试用户配置获取"""
        with patch('server.resources.config_data.load_user_config') as mock_load:
            mock_load.return_value = {
                "theme": "dark",
                "language": "zh-CN",
                "notifications": True
            }
            
            result = get_config_data("user_config")
            
            assert result["theme"] == "dark"
            assert result["language"] == "zh-CN"
            assert result["notifications"] is True

    def test_config_validation(self):
        """测试配置验证"""
        from server.resources.config_data import validate_config
        
        valid_config = {
            "app_name": "Test App",
            "version": "1.0.0",
            "debug": False
        }
        
        # 应该不抛出异常
        validate_config(valid_config)
        
        # 测试无效配置
        invalid_config = {
            "app_name": "",  # 空名称
            "version": "invalid-version"  # 无效版本格式
        }
        
        with pytest.raises(ValueError):
            validate_config(invalid_config)
```

## 💬 MCP Prompts 测试

```python
# tests/test_prompts.py
"""
MCP 提示测试
"""

import pytest
from server.prompts.code_review import generate_code_review_prompt
from server.prompts.data_analysis import generate_data_analysis_prompt


class TestCodeReviewPrompts:
    """代码审查提示测试"""

    def test_code_review_basic(self):
        """测试基本代码审查提示"""
        context = {
            "code": "def hello():\n    print('Hello, World!')",
            "language": "python",
            "focus": "general"
        }
        
        prompt = generate_code_review_prompt(context)
        
        assert "代码审查" in prompt
        assert "python" in prompt.lower()
        assert "def hello" in prompt

    def test_code_review_security_focus(self):
        """测试安全性审查提示"""
        context = {
            "code": "import os\nos.system(user_input)",
            "language": "python",
            "focus": "security"
        }
        
        prompt = generate_code_review_prompt(context)
        
        assert "安全" in prompt
        assert "os.system" in prompt

    def test_code_review_missing_context(self):
        """测试缺少必需上下文"""
        context = {
            "language": "python"
            # 缺少 "code" 字段
        }
        
        with pytest.raises(ValueError, match="Missing required context"):
            generate_code_review_prompt(context)

    @pytest.mark.parametrize("language,expected_keywords", [
        ("python", ["PEP 8", "类型提示"]),
        ("javascript", ["ESLint", "异步"]),
        ("java", ["命名规范", "异常处理"])
    ])
    def test_language_specific_prompts(self, language, expected_keywords):
        """测试语言特定的提示内容"""
        context = {
            "code": "// Sample code",
            "language": language,
            "focus": "general"
        }
        
        prompt = generate_code_review_prompt(context)
        
        # 检查是否包含语言特定的关键词
        for keyword in expected_keywords:
            assert keyword in prompt


class TestDataAnalysisPrompts:
    """数据分析提示测试"""

    def test_statistical_analysis_prompt(self):
        """测试统计分析提示"""
        context = {
            "data_type": "numerical",
            "analysis_type": "statistical",
            "columns": ["age", "income", "score"],
            "sample_size": 1000
        }
        
        prompt = generate_data_analysis_prompt(context)
        
        assert "统计分析" in prompt
        assert "age" in prompt
        assert "income" in prompt
        assert "1000" in prompt

    def test_prediction_model_prompt(self):
        """测试预测模型提示"""
        context = {
            "data_type": "mixed",
            "analysis_type": "prediction",
            "target_variable": "sales",
            "features": ["price", "marketing_budget", "season"]
        }
        
        prompt = generate_data_analysis_prompt(context)
        
        assert "预测" in prompt
        assert "sales" in prompt
        assert "特征" in prompt

    def test_prompt_length_limit(self):
        """测试提示长度限制"""
        context = {
            "data_type": "text",
            "analysis_type": "sentiment",
            "description": "x" * 10000  # 超长描述
        }
        
        prompt = generate_data_analysis_prompt(context)
        
        # 确保提示不会过长
        assert len(prompt) < 8000

    def test_invalid_analysis_type(self):
        """测试无效分析类型"""
        context = {
            "data_type": "numerical",
            "analysis_type": "invalid_type"
        }
        
        with pytest.raises(ValueError, match="Unsupported analysis type"):
            generate_data_analysis_prompt(context)
```

## 🌐 HTTP API 集成测试

```python
# tests/test_integration.py
"""
集成测试
"""

import pytest
import httpx
from fastapi.testclient import TestClient
from server.main import create_app


@pytest.fixture
def test_client():
    """测试客户端 fixture"""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def async_client():
    """异步测试客户端 fixture"""
    app = create_app()
    return httpx.AsyncClient(app=app, base_url="http://test")


class TestHealthEndpoints:
    """健康检查端点测试"""

    def test_health_check(self, test_client):
        """测试健康检查端点"""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_info_endpoint(self, test_client):
        """测试信息端点"""
        response = test_client.get("/info")
        
        assert response.status_code == 200
        data = response.json()
        assert "app_name" in data
        assert "version" in data
        assert "environment" in data


class TestMCPAPIEndpoints:
    """MCP API 端点测试"""

    def test_tools_list(self, test_client):
        """测试工具列表端点"""
        response = test_client.get("/api/tools")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # 检查工具结构
        tool = data[0]
        assert "name" in tool
        assert "description" in tool

    def test_resources_list(self, test_client):
        """测试资源列表端点"""
        response = test_client.get("/api/resources")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_convert_text(self, test_client):
        """测试文本转换端点"""
        payload = {
            "text": "Hello World",
            "operation": "uppercase"
        }
        
        response = test_client.post("/api/convert", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "HELLO WORLD"

    def test_convert_invalid_operation(self, test_client):
        """测试无效转换操作"""
        payload = {
            "text": "Hello World",
            "operation": "invalid_op"
        }
        
        response = test_client.post("/api/convert", json=payload)
        
        assert response.status_code == 400


class TestMCPProtocolIntegration:
    """MCP 协议集成测试"""

    @pytest.mark.asyncio
    async def test_mcp_tools_list(self, async_client):
        """测试 MCP 工具列表"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }
        
        response = await async_client.post("/mcp", json=mcp_request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert "result" in data
        assert "tools" in data["result"]

    @pytest.mark.asyncio
    async def test_mcp_tool_call(self, async_client):
        """测试 MCP 工具调用"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "add",
                "arguments": {
                    "a": 5,
                    "b": 3
                }
            }
        }
        
        response = await async_client.post("/mcp", json=mcp_request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"]["content"][0]["text"] == "8"

    @pytest.mark.asyncio
    async def test_mcp_resources_list(self, async_client):
        """测试 MCP 资源列表"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list"
        }
        
        response = await async_client.post("/mcp", json=mcp_request)
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "resources" in data["result"]

    @pytest.mark.asyncio
    async def test_mcp_resource_read(self, async_client):
        """测试 MCP 资源读取"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "resources/read",
            "params": {
                "uri": "system://cpu"
            }
        }
        
        response = await async_client.post("/mcp", json=mcp_request)
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "contents" in data["result"]

    @pytest.mark.asyncio
    async def test_mcp_invalid_method(self, async_client):
        """测试无效 MCP 方法"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "invalid/method"
        }
        
        response = await async_client.post("/mcp", json=mcp_request)
        
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == -32601  # Method not found
```

## 🎭 模拟和 Fixtures

### 1. 外部服务模拟

```python
# tests/mocks.py
"""
测试模拟工具
"""

from unittest.mock import Mock, AsyncMock
import pytest


class MockHTTPClient:
    """模拟 HTTP 客户端"""
    
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.call_count = 0
    
    async def get(self, url, **kwargs):
        self.call_count += 1
        
        if url in self.responses:
            response = Mock()
            response.json.return_value = self.responses[url]
            response.status_code = 200
            return response
        
        # 默认响应
        response = Mock()
        response.json.return_value = {"status": "ok"}
        response.status_code = 200
        return response


@pytest.fixture
def mock_weather_api():
    """模拟天气 API"""
    responses = {
        "https://api.weather.com/current": {
            "temperature": 25,
            "humidity": 60,
            "description": "Sunny"
        }
    }
    return MockHTTPClient(responses)


@pytest.fixture
def mock_database():
    """模拟数据库"""
    db = Mock()
    db.users = []
    
    def add_user(user):
        db.users.append(user)
        return len(db.users)
    
    def get_user(user_id):
        if 0 <= user_id < len(db.users):
            return db.users[user_id]
        return None
    
    db.add_user = add_user
    db.get_user = get_user
    
    return db
```

### 2. 数据生成器

```python
# tests/factories.py
"""
测试数据工厂
"""

import factory
from faker import Faker
from datetime import datetime

fake = Faker()


class UserFactory(factory.Factory):
    """用户数据工厂"""
    
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: n)
    name = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    age = factory.LazyFunction(lambda: fake.random_int(18, 80))
    created_at = factory.LazyFunction(datetime.now)


class DocumentFactory(factory.Factory):
    """文档数据工厂"""
    
    class Meta:
        model = dict
    
    title = factory.LazyFunction(fake.sentence)
    content = factory.LazyFunction(fake.text)
    author = factory.SubFactory(UserFactory)
    tags = factory.LazyFunction(lambda: fake.words(3))


# 使用示例
@pytest.fixture
def sample_users():
    """生成示例用户数据"""
    return UserFactory.build_batch(5)


@pytest.fixture
def sample_document():
    """生成示例文档数据"""
    return DocumentFactory.build()
```

## 📊 性能测试

```python
# tests/test_performance.py
"""
性能测试
"""

import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed


class TestPerformance:
    """性能测试类"""

    def test_tool_execution_time(self):
        """测试工具执行时间"""
        from server.tools.calculator import calculate_bmi
        
        start_time = time.time()
        
        # 执行多次测试
        for _ in range(100):
            calculate_bmi(70, 1.75)
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 100
        
        # 断言平均执行时间小于 1ms
        assert avg_time < 0.001

    @pytest.mark.slow
    def test_concurrent_tool_calls(self):
        """测试并发工具调用"""
        from server.tools.text_processing import count_words
        
        text = "This is a test text for concurrent processing"
        
        def call_tool():
            return count_words(text)
        
        start_time = time.time()
        
        # 并发执行
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(call_tool) for _ in range(100)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        
        # 验证所有结果一致
        assert all(r["words"] == results[0]["words"] for r in results)
        
        # 验证并发执行时间合理
        assert end_time - start_time < 5.0

    @pytest.mark.asyncio
    async def test_async_performance(self):
        """测试异步性能"""
        from server.tools.api_client import fetch_data
        
        async def mock_fetch():
            await asyncio.sleep(0.1)  # 模拟网络延迟
            return {"data": "test"}
        
        start_time = time.time()
        
        # 并发执行异步任务
        tasks = [mock_fetch() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        
        # 验证并发执行比串行快
        assert end_time - start_time < 0.5  # 应该接近 0.1 秒而不是 1 秒
        assert len(results) == 10

    def test_memory_usage(self):
        """测试内存使用"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # 执行一些操作
        from server.tools.file_operations import read_file, write_file
        
        for i in range(100):
            content = f"Test content {i}" * 100
            write_file(f"temp_{i}.txt", content)
            read_file(f"temp_{i}.txt")
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 内存增长应该在合理范围内（小于 50MB）
        assert memory_increase < 50 * 1024 * 1024
```

## 🚀 CI/CD 测试配置

### 1. GitHub Actions 配置

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Run unit tests
      run: |
        pytest tests/test_tools.py tests/test_resources.py tests/test_prompts.py -v

    - name: Run integration tests
      run: |
        pytest tests/test_integration.py -v

    - name: Run performance tests
      run: |
        pytest tests/test_performance.py -v -m "not slow"

    - name: Generate coverage report
      run: |
        pytest --cov=server --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### 2. 测试数据管理

```python
# tests/test_data.py
"""
测试数据管理
"""

import json
from pathlib import Path


class TestDataManager:
    """测试数据管理器"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
    
    def load_json(self, filename: str) -> dict:
        """加载 JSON 测试数据"""
        file_path = self.data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Test data file not found: {filename}")
        
        with file_path.open('r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_json(self, filename: str, data: dict) -> None:
        """保存 JSON 测试数据"""
        file_path = self.data_dir / filename
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


@pytest.fixture
def test_data_manager():
    """测试数据管理器 fixture"""
    return TestDataManager()


# 使用示例
def test_with_json_data(test_data_manager):
    """使用 JSON 测试数据的测试"""
    user_data = test_data_manager.load_json("sample_users.json")
    
    # 使用测试数据进行测试
    assert len(user_data) > 0
    assert "name" in user_data[0]
```

## 📋 测试最佳实践

### 1. 测试组织原则

- **AAA 模式**: Arrange（准备）、Act（执行）、Assert（断言）
- **单一职责**: 每个测试只验证一个功能点
- **独立性**: 测试之间不应有依赖关系
- **可重复性**: 测试结果应该一致和可预测

### 2. 测试命名规范

```python
# ✅ 好的测试命名
def test_calculate_bmi_with_valid_input_returns_correct_result():
    pass

def test_read_file_with_nonexistent_file_raises_file_not_found():
    pass

def test_extract_emails_from_text_with_multiple_emails_returns_all():
    pass

# ❌ 不好的测试命名
def test_bmi():
    pass

def test_file():
    pass

def test_email():
    pass
```

### 3. 断言最佳实践

```python
# ✅ 具体的断言
assert result["status"] == "success"
assert len(emails) == 2
assert "error" not in response

# ✅ 使用 pytest 的专用断言
assert result == pytest.approx(22.86, rel=1e-2)
assert "test@example.com" in emails

# ✅ 异常断言
with pytest.raises(ValueError, match="Weight must be positive"):
    calculate_bmi(-70, 1.75)

# ❌ 模糊的断言
assert result
assert emails
assert response
```

### 4. 测试数据管理

```python
# ✅ 使用 fixtures 管理测试数据
@pytest.fixture
def sample_user():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30
    }

# ✅ 参数化测试
@pytest.mark.parametrize("weight,height,expected", [
    (70, 1.75, 22.86),
    (60, 1.60, 23.44),
    (80, 1.80, 24.69)
])
def test_bmi_calculation(weight, height, expected):
    result = calculate_bmi(weight, height)
    assert result["bmi"] == pytest.approx(expected, rel=1e-2)
```

## 🔍 调试和故障排除

### 1. 测试调试技巧

```python
# 使用 pytest 的调试功能
pytest -v -s  # 显示详细输出
pytest --pdb  # 失败时进入调试器
pytest -k "test_name"  # 运行特定测试

# 在测试中添加调试信息
def test_complex_logic():
    result = complex_function(input_data)
    
    # 调试输出
    print(f"Input: {input_data}")
    print(f"Result: {result}")
    
    assert result.is_valid()
```

### 2. 常见问题解决

```python
# 问题：异步测试失败
# 解决：确保使用正确的异步标记
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None

# 问题：文件路径问题
# 解决：使用相对于测试文件的路径
test_file = Path(__file__).parent / "data" / "test.txt"

# 问题：时间相关测试不稳定
# 解决：使用 freezegun 固定时间
from freezegun import freeze_time

@freeze_time("2023-01-01 12:00:00")
def test_time_dependent_function():
    result = get_current_time_info()
    assert result["hour"] == 12
```