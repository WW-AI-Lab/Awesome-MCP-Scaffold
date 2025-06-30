# 🎯 Cursor IDE Usage Guide

This guide provides a detailed introduction on how to fully utilize the features and configurations of **Awesome MCP Scaffold** in Cursor IDE.

## 🌟 Why Choose Cursor?

Cursor is a modern IDE designed specifically for AI-assisted development, perfectly integrated with the MCP protocol:

- **Native MCP support**: Direct connection and usage of MCP servers
- **Smart code completion**: AI suggestions based on context
- **Natural language programming**: Describe requirements in natural language, AI generates code
- **Real-time collaboration**: Seamless collaboration with AI assistant

## 📁 Project Configuration

### Cursor Rules Configuration

The project includes pre-configured Cursor rule files:

```
.cursor/
├── rules/
│   ├── mcp-development-guide.mdc     # MCP development guide
│   ├── mcp-testing-patterns.mdc     # Testing patterns guide
│   └── streamable-http-production.mdc # Production deployment guide
```

These rules automatically tell Cursor:
- MCP best practices
- Code structure specifications
- Testing strategies
- Deployment patterns

### Auto-Applied Rules

When you open the project in Cursor, the following rules automatically take effect:

1. **MCP server development standards**
2. **FastMCP framework usage guidance**
3. **Streamable HTTP transport optimization**
4. **Test-driven development patterns**
5. **Production deployment best practices**

## 🔧 Configure MCP Server

### 1. Add MCP Server in Cursor Settings

Open Cursor settings (`Cmd/Ctrl + ,`), find the MCP configuration section, and add:

```json
{
  "mcpServers": {
    "awesome-mcp-scaffold": {
      "command": "python",
      "args": ["-m", "server.main"],
      "cwd": "/path/to/your/Awesome-MCP-Scaffold",
      "env": {
        "TRANSPORT": "stdio",
        "ENVIRONMENT": "development",
        "DEBUG": "true"
      }
    }
  }
}
```

### 2. Verify Connection

In Cursor, press `Cmd/Ctrl + Shift + P`, search for "MCP", you should see:
- **MCP: Connect to Server**
- **MCP: List Tools**
- **MCP: List Resources**

## 🛠️ Using MCP Features

### Calculator Tool

In Cursor, you can directly ask AI to perform calculations:

```
User: "Help me calculate BMI, weight 70kg, height 1.75m"
AI: Let me calculate BMI for you...
[Calls calculate_bmi tool]
Result: BMI = 22.86 (Normal weight)
```

### Text Processing

```
User: "Analyze the statistics of this text: 'Hello World! This is a test.'"
AI: Let me analyze text statistics...
[Calls text_statistics tool]
Result: 
- Word count: 6
- Character count: 29
- Sentence count: 2
- Average word length: 4.83
```

### File Operations

```
User: "Create a JSON file in the workspace directory containing user data"
AI: Let me create the JSON file...
[Calls write_json_file tool]
Result: File created at workspace/users.json
```

### System Information

```
User: "Show current system memory usage"
AI: Let me get system information...
[Reads system://memory resource]
Result: Memory usage 45%, available memory 8.2GB
```

## 🎨 Development Workflow

### 1. Create New Tool

Using Cursor's natural language programming:

```
User: "Create a new MCP tool for generating random passwords"

AI will automatically:
1. Create new file in server/tools/
2. Implement password generation logic
3. Register tool to main module
4. Add corresponding tests
```

### 2. Code Review

```
User: "Review the code quality of this function"

AI will use the built-in code_review prompt template to provide:
- Code quality analysis
- Performance optimization suggestions
- Security checks
- Best practice recommendations
```

### 3. Test Generation

```
User: "Generate unit tests for this tool"

AI will:
1. Analyze tool functionality
2. Generate test cases
3. Include boundary condition tests
4. Add error handling tests
```

## 🚀 Advanced Features

### Smart Refactoring

Cursor can understand MCP architecture and provide intelligent refactoring suggestions:

```
User: "Refactor this tool to better comply with MCP best practices"

AI will:
- Analyze current code structure
- Apply MCP development standards
- Optimize error handling
- Improve docstrings
```

### Automated Testing

```
User: "Run all tests and fix failed tests"

AI will:
1. Execute make test
2. Analyze test results
3. Automatically fix simple test failures
4. Provide solutions for complex issues
```

### Deployment Optimization

```
User: "Optimize this MCP server for production deployment"

AI will:
- Apply production configuration best practices
- Optimize performance settings
- Add monitoring and logging
- Configure security settings
```

## 🎯 Real-World Use Cases

### Scenario 1: API Integration

```
User: "Integrate OpenWeatherMap API as an MCP tool"

AI workflow:
1. Create new tool module
2. Implement API call logic
3. Add error handling and retry
4. Create corresponding tests
5. Update documentation
```

### Scenario 2: Data Analysis

```
User: "Create a data analysis tool that can process CSV files"

AI will:
1. Implement CSV reading tool
2. Add statistical data analysis
3. Create visualization suggestions
4. Integrate into MCP framework
```

### Scenario 3: Automation Tasks

```
User: "Create a scheduled task tool that can periodically clean temporary files"

AI will:
1. Design task scheduling system
2. Implement file cleanup logic
3. Add configuration management
4. Create monitoring functionality
```

## 🔍 Debugging Tips

### 1. MCP Connection Debugging

If there are MCP connection issues:

```
User: "MCP server connection failed, help me debug"

AI will check:
- Server process status
- Configuration file correctness
- Port occupation status
- Log error information
```

### 2. Tool Debugging

```
User: "This tool returns an error, help me find the problem"

AI will:
1. Analyze error stack
2. Check input parameters
3. Verify tool logic
4. Provide fix suggestions
```

### 3. Performance Debugging

```
User: "Server response is slow, help me optimize performance"

AI will:
1. Analyze performance bottlenecks
2. Check resource usage
3. Optimize algorithm complexity
4. Add caching mechanisms
```

## 📚 Learning Resources

### Cursor-Specific Features

- **@** symbol: Reference specific files or functions
- **Tab completion**: AI-driven code completion
- **Cmd+K**: Natural language editing
- **Cmd+L**: Chat with AI

### MCP Integration

- Use `@mcp` prefix to reference MCP functionality
- Call tools directly through Cursor Chat
- View MCP server status in real-time

## 🎉 Best Practices

### 1. Effective Prompts

```
✅ Good prompt:
"Create an MCP tool for calculating days between two dates, including input validation and error handling"

❌ Vague prompt:
"Make a date tool"
```

### 2. Incremental Development

```
1. Create basic functionality first
2. Add error handling
3. Improve documentation
4. Add tests
5. Performance optimization
```

### 3. Leverage Context

```
User: "Based on the tool just created, create another related tool"

AI will understand context and create related functionality
```

## 🚨 Common Issues

### Q: Cursor cannot recognize MCP server?

**Solution:**
1. Check MCP server configuration path
2. Confirm server is running
3. Restart Cursor IDE
4. Check Cursor logs

### Q: AI-suggested code doesn't comply with project standards?

**Solution:**
1. Confirm `.cursor/rules` files exist
2. Explicitly mention standard requirements in prompts
3. Use `@rules` to reference specific rules

### Q: How to make AI better understand project structure?

**Solution:**
1. Use `@codebase` to reference entire project
2. Mention relevant files in conversation
3. Maintain clear project documentation 