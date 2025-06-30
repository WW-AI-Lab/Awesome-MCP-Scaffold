# 🤝 贡献指南

感谢您对 **Awesome MCP Scaffold** 项目的关注！我们欢迎任何形式的贡献。

## 🎯 贡献方式

### 1. 代码贡献
- 修复 Bug
- 添加新功能
- 改进性能
- 优化代码结构

### 2. 文档贡献
- 完善文档
- 翻译文档
- 添加示例
- 修正错误

### 3. 问题反馈
- 报告 Bug
- 提出功能请求
- 分享使用经验
- 提供建议

## 🚀 开始贡献

### 1. Fork 项目

点击 GitHub 页面右上角的 "Fork" 按钮。

### 2. 克隆项目

```bash
git clone https://github.com/your-username/Awesome-MCP-Scaffold.git
cd Awesome-MCP-Scaffold
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 4. 安装开发环境

```bash
make install-dev
```

### 5. 进行开发

遵循项目的编码规范和最佳实践。

### 6. 运行测试

```bash
make test
make lint
```

### 7. 提交更改

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 8. 创建 Pull Request

在 GitHub 上创建 Pull Request，描述您的更改。

## 📝 编码规范

### Python 代码风格
- 使用 **ruff** 进行代码格式化
- 使用 **mypy** 进行类型检查
- 遵循 **PEP 8** 规范
- 添加适当的文档字符串

### 提交信息规范
使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**类型 (type):**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行的变动）
- `refactor`: 重构（即不是新增功能，也不是修改bug的代码变动）
- `test`: 增加测试
- `chore`: 构建过程或辅助工具的变动

**示例:**
```
feat(tools): add weather API integration
fix(server): resolve memory leak in resource handler
docs(readme): update installation instructions
```

## 🧪 测试指南

### 运行测试
```bash
# 运行所有测试
make test

# 运行特定测试
pytest tests/test_tools.py -v

# 运行覆盖率测试
pytest --cov=server --cov-report=html
```

### 编写测试
- 为新功能添加测试
- 确保测试覆盖率 > 80%
- 使用描述性的测试名称
- 测试边界条件和错误情况

## 📚 文档指南

### 文档结构
- 使用 Markdown 格式
- 添加适当的标题层级
- 包含代码示例
- 提供清晰的说明

### API 文档
- 使用 Python 文档字符串
- 描述参数和返回值
- 提供使用示例

## 🔍 代码审查

### 审查清单
- [ ] 代码风格符合规范
- [ ] 测试通过且覆盖率足够
- [ ] 文档完整且准确
- [ ] 性能影响可接受
- [ ] 安全性考虑充分

### 反馈处理
- 积极回应审查意见
- 及时修复问题
- 保持友好的沟通

## 🐛 Bug 报告

### 报告模板
```markdown
**Bug 描述**
简要描述遇到的问题。

**复现步骤**
1. 执行 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**期望行为**
描述您期望发生的情况。

**实际行为**
描述实际发生的情况。

**环境信息**
- OS: [e.g. macOS 12.0]
- Python: [e.g. 3.11.0]
- MCP SDK: [e.g. 1.10.1]

**附加信息**
添加任何其他有助于解决问题的信息。
```

## ✨ 功能请求

### 请求模板
```markdown
**功能描述**
简要描述您希望添加的功能。

**使用场景**
描述这个功能的使用场景和价值。

**解决方案**
描述您期望的解决方案。

**替代方案**
描述您考虑过的其他解决方案。

**附加信息**
添加任何其他相关信息。
```

## 🎉 认可贡献者

我们使用 [All Contributors](https://allcontributors.org/) 来认可所有贡献者。

## 📞 联系我们

- **GitHub Issues**: [项目问题](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/issues)
- **GitHub Discussions**: [项目讨论](https://github.com/WW-AI-Lab/Awesome-MCP-Scaffold/discussions)
- **邮箱**: toxingwang@gmail.com

## 📄 许可证

通过贡献代码，您同意您的贡献将在 [MIT 许可证](LICENSE) 下授权。

---

**感谢您的贡献！** 🙏 