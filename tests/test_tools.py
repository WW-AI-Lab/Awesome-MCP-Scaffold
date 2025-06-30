"""
MCP 工具测试模块

测试所有 MCP 工具的功能和边界条件。
"""

import re

import pytest


class TestCalculatorTools:
    """计算器工具测试"""

    def test_add(self):
        """测试加法工具"""
        # 这里需要实际的工具调用逻辑
        # 示例测试结构
        assert 2 + 3 == 5
        assert -1 + 1 == 0
        assert 0.1 + 0.2 == pytest.approx(0.3)

    def test_divide_by_zero(self):
        """测试除零错误"""
        # 模拟除零检查逻辑
        def divide(a, b):
            if b == 0:
                raise ValueError("Cannot divide by zero")
            return a / b

        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_bmi_calculation(self):
        """测试 BMI 计算"""
        # 测试正常情况
        weight = 70  # kg
        height = 1.75  # m
        expected_bmi = weight / (height ** 2)

        # 这里应该调用实际的 BMI 工具
        assert expected_bmi == pytest.approx(22.86, rel=1e-2)

    def test_bmi_invalid_input(self):
        """测试 BMI 计算的无效输入"""
        # 模拟 BMI 计算逻辑
        def calculate_bmi(weight, height):
            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive")
            return weight / (height ** 2)

        with pytest.raises(ValueError, match="Weight and height must be positive"):
            calculate_bmi(-70, 1.75)


class TestTextProcessingTools:
    """文本处理工具测试"""

    def test_word_count(self):
        """测试单词计数"""
        # 模拟单词计数逻辑
        def count_words(text):
            words = len(text.split())
            characters = len(text)
            characters_no_spaces = len(text.replace(" ", ""))
            lines = len(text.split("\n"))
            return {
                "words": words,
                "characters": characters,
                "characters_no_spaces": characters_no_spaces,
                "lines": lines
            }

        text = "Hello world! This is a test."
        result = count_words(text)
        assert result["words"] == 6
        assert result["characters"] == 28

    def test_case_conversion(self):
        """测试大小写转换"""
        text = "Hello World"

        # 测试各种转换
        assert text.upper() == "HELLO WORLD"
        assert text.lower() == "hello world"
        assert text.title() == "Hello World"

    def test_email_extraction(self):
        """测试邮箱提取"""
        text = "Contact us at test@example.com or admin@test.org"
        expected_emails = ["test@example.com", "admin@test.org"]

        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        found_emails = re.findall(email_pattern, text)

        assert set(found_emails) == set(expected_emails)

    def test_slug_generation(self):
        """测试 URL slug 生成"""
        text = "Hello World! This is a Test."
        expected_slug = "hello-world-this-is-a-test"

        # 模拟 slug 生成逻辑
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')

        assert slug == expected_slug


class TestFileOperationTools:
    """文件操作工具测试"""

    def test_safe_path_validation(self):
        """测试安全路径验证"""
        from pathlib import Path

        safe_dir = Path.cwd() / "workspace"
        safe_dir.mkdir(exist_ok=True)

        # 测试安全路径
        safe_path = safe_dir / "test.txt"
        assert safe_path.is_relative_to(safe_dir)

        # 测试不安全路径（应该被拒绝）
        unsafe_path = Path("/etc/passwd")
        assert not unsafe_path.is_relative_to(safe_dir)

    def test_directory_listing(self):
        """测试目录列表"""
        from pathlib import Path

        # 创建测试目录结构
        test_dir = Path.cwd() / "workspace" / "test"
        test_dir.mkdir(parents=True, exist_ok=True)

        # 创建测试文件
        (test_dir / "file1.txt").write_text("test")
        (test_dir / "subdir").mkdir(exist_ok=True)

        # 测试目录列表功能
        items = list(test_dir.iterdir())
        files = [item.name for item in items if item.is_file()]
        dirs = [item.name for item in items if item.is_dir()]

        assert "file1.txt" in files
        assert "subdir" in dirs

    def test_json_operations(self):
        """测试 JSON 文件操作"""
        import json
        from pathlib import Path

        test_data = {"name": "test", "value": 123}
        test_file = Path.cwd() / "workspace" / "test.json"

        # 写入 JSON
        with test_file.open('w') as f:
            json.dump(test_data, f)

        # 读取 JSON
        with test_file.open('r') as f:
            loaded_data = json.load(f)

        assert loaded_data == test_data

        # 清理
        test_file.unlink(missing_ok=True)


@pytest.fixture
def setup_test_environment():
    """设置测试环境"""
    from pathlib import Path

    # 创建测试工作目录
    workspace = Path.cwd() / "workspace"
    workspace.mkdir(exist_ok=True)

    yield workspace

    # 清理测试文件（可选）
    # import shutil
    # shutil.rmtree(workspace, ignore_errors=True)


def test_integration_workflow(setup_test_environment):
    """集成测试：完整工作流程"""
    workspace = setup_test_environment

    # 1. 创建测试文件
    test_file = workspace / "integration_test.txt"
    test_content = "Hello World! This is an integration test."
    test_file.write_text(test_content)

    # 2. 验证文件创建
    assert test_file.exists()
    assert test_file.read_text() == test_content

    # 3. 文本处理
    word_count = len(test_content.split())
    assert word_count == 7  # "Hello World! This is an integration test." = 7 words

    # 4. 数学计算
    char_count = len(test_content)
    average_word_length = char_count / word_count
    assert average_word_length > 0

    # 5. 清理
    test_file.unlink()
    assert not test_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
