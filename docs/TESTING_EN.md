# 🧪 Testing Guide

> **Comprehensive Testing Strategy for MCP Server Scaffold - Ensuring Code Quality and Functional Reliability**

## 🎯 Testing Strategy Overview

This document provides a complete testing guide for the **Awesome-MCP-Scaffold** project, covering special testing requirements and best practices for the MCP protocol. As a scaffold project, these testing patterns will guide MCP servers developed based on this template.

## 📊 Testing Architecture Layers

### Testing Pyramid

```
    🔺 E2E Testing (5%)
       ├── MCP Client Integration Tests
       └── Complete Workflow Verification
    
    🔷 Integration Testing (25%)
       ├── HTTP API Endpoint Tests
       ├── MCP Protocol Interaction Tests
       └── Database/External Service Integration
    
    🔶 Unit Testing (70%)
       ├── Tools Function Tests
       ├── Resources Logic Tests
       ├── Prompts Template Tests
       └── Utility Function Tests
```

### Test Coverage Targets

| Component Type | Coverage Target | Key Test Content |
|----------------|----------------|------------------|
| **MCP Tools** | 95%+ | Function correctness, input validation, error handling |
| **MCP Resources** | 90%+ | Data retrieval, caching mechanisms, permission control |
| **MCP Prompts** | 85%+ | Template rendering, parameter validation, output format |
| **HTTP Routes** | 90%+ | Endpoint responses, status codes, data format |
| **Configuration Management** | 80%+ | Environment variables, default values, validation logic |

## 🛠️ Test Environment Configuration

### 1. Test Dependencies Installation

```bash
# Install test-related dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock httpx
pip install faker factory-boy freezegun

# Or use project configuration
pip install -e ".[dev]"
```

### 2. pytest Configuration

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
    "unit: Unit tests",
    "integration: Integration tests", 
    "e2e: End-to-end tests",
    "slow: Slow tests",
    "external: Tests requiring external services"
]
```

### 3. Test Environment Isolation

```python
# tests/conftest.py
"""
Test configuration and fixtures
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock

from server.config import Settings


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment variables"""
    # Create temporary test directory
    test_dir = tempfile.mkdtemp()
    
    # Set test environment variables
    os.environ.update({
        "ENVIRONMENT": "testing",
        "LOG_LEVEL": "DEBUG",
        "TEST_DATA_DIR": test_dir,
        "DATABASE_URL": "sqlite:///test.db",
        "REDIS_URL": "redis://localhost:6379/1"
    })
    
    yield test_dir
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture
def test_settings():
    """Test configuration fixture"""
    return Settings(
        environment="testing",
        debug=True,
        log_level="DEBUG"
    )


@pytest.fixture
def workspace_dir():
    """Workspace directory fixture"""
    workspace = Path.cwd() / "workspace"
    workspace.mkdir(exist_ok=True)
    
    yield workspace
    
    # Optional: cleanup test files
    # import shutil
    # shutil.rmtree(workspace, ignore_errors=True)


@pytest.fixture
def sample_json_data():
    """Sample JSON data"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30,
        "skills": ["Python", "MCP", "Testing"]
    }


@pytest.fixture
def mock_external_api():
    """Mock external API"""
    mock = Mock()
    mock.get.return_value.json.return_value = {"status": "success"}
    mock.get.return_value.status_code = 200
    return mock
```

## 🔧 MCP Tools Testing

### 1. Basic Tool Testing

```python
# tests/test_tools.py
"""
MCP Tools Testing
"""

import pytest
from unittest.mock import patch, Mock
from server.tools.calculator import add, subtract, calculate_bmi
from server.tools.text_processing import count_words, extract_emails
from server.tools.file_operations import read_file, write_file


class TestCalculatorTools:
    """Calculator tools testing"""

    def test_add_positive_numbers(self):
        """Test positive number addition"""
        result = add(5, 3)
        assert result == 8

    def test_add_negative_numbers(self):
        """Test negative number addition"""
        result = add(-5, -3)
        assert result == -8

    def test_add_mixed_numbers(self):
        """Test mixed positive and negative number addition"""
        result = add(5, -3)
        assert result == 2

    def test_add_zero(self):
        """Test addition with zero"""
        result = add(0, 5)
        assert result == 5
``` 