"""
代码审查提示模块

提供代码审查和分析相关的 MCP 提示模板。
"""

from mcp.server.fastmcp import FastMCP


def register_code_prompts(mcp: FastMCP) -> None:
    """注册代码审查相关的提示模板"""

    @mcp.prompt(title="Code Review")
    def code_review(code: str, language: str = "python") -> str:
        """
        Generate a prompt for comprehensive code review.
        
        Args:
            code: The code to review
            language: Programming language (default: python)
        """
        return f"""Please conduct a thorough code review of the following {language} code:

```{language}
{code}
```

Please analyze the code for:

1. **Code Quality**:
   - Readability and clarity
   - Naming conventions
   - Code structure and organization

2. **Best Practices**:
   - Language-specific conventions
   - Design patterns usage
   - SOLID principles adherence

3. **Performance**:
   - Time complexity analysis
   - Memory usage considerations
   - Potential bottlenecks

4. **Security**:
   - Input validation
   - Potential vulnerabilities
   - Security best practices

5. **Maintainability**:
   - Code documentation
   - Error handling
   - Testability

6. **Bugs and Issues**:
   - Logic errors
   - Edge cases
   - Potential runtime issues

Please provide specific suggestions for improvement with examples where applicable."""

    @mcp.prompt(title="Bug Analysis")
    def bug_analysis(error_message: str, code_context: str = "") -> str:
        """
        Generate a prompt for bug analysis and debugging.
        
        Args:
            error_message: The error message or description
            code_context: Optional code context where the bug occurs
        """
        prompt = f"""Please help analyze and debug the following issue:

**Error/Issue Description:**
{error_message}
"""

        if code_context:
            prompt += f"""
**Code Context:**
```
{code_context}
```
"""

        prompt += """
Please provide:

1. **Root Cause Analysis**:
   - What is causing this issue?
   - Why is it happening?

2. **Debugging Steps**:
   - How to reproduce the issue
   - What to check or investigate

3. **Solution Options**:
   - Immediate fixes
   - Long-term solutions
   - Alternative approaches

4. **Prevention**:
   - How to prevent similar issues
   - Best practices to follow

5. **Testing Strategy**:
   - How to verify the fix
   - Test cases to add

Please provide specific, actionable recommendations."""

        return prompt

    @mcp.prompt(title="Code Optimization")
    def code_optimization(code: str, optimization_goal: str = "performance") -> str:
        """
        Generate a prompt for code optimization.
        
        Args:
            code: The code to optimize
            optimization_goal: Optimization target (performance, memory, readability)
        """
        return f"""Please optimize the following code with a focus on {optimization_goal}:

```
{code}
```

**Optimization Goals:**
- Primary: {optimization_goal}
- Maintain functionality
- Preserve readability (unless readability is the goal)

Please provide:

1. **Analysis of Current Code**:
   - Performance characteristics
   - Resource usage
   - Complexity analysis

2. **Optimization Opportunities**:
   - Specific areas for improvement
   - Algorithmic improvements
   - Data structure optimizations

3. **Optimized Code**:
   - Improved version with explanations
   - Key changes highlighted

4. **Trade-offs**:
   - What was gained vs. what was sacrificed
   - When to use each approach

5. **Benchmarking**:
   - How to measure improvements
   - Expected performance gains

Please provide working, tested code examples."""

    @mcp.prompt(title="Architecture Review")
    def architecture_review(description: str, requirements: str = "") -> str:
        """
        Generate a prompt for software architecture review.
        
        Args:
            description: Description of the current architecture
            requirements: System requirements and constraints
        """
        prompt = f"""Please review the following software architecture:

**Architecture Description:**
{description}
"""

        if requirements:
            prompt += f"""
**Requirements:**
{requirements}
"""

        prompt += """
Please analyze and provide feedback on:

1. **Design Principles**:
   - SOLID principles adherence
   - Separation of concerns
   - Single responsibility

2. **Scalability**:
   - Horizontal and vertical scaling
   - Performance bottlenecks
   - Resource utilization

3. **Maintainability**:
   - Code organization
   - Modularity
   - Dependency management

4. **Reliability**:
   - Fault tolerance
   - Error handling
   - Recovery mechanisms

5. **Security**:
   - Security architecture
   - Data protection
   - Access control

6. **Technology Choices**:
   - Technology stack evaluation
   - Tool and framework selection
   - Integration patterns

7. **Recommendations**:
   - Improvement suggestions
   - Alternative approaches
   - Migration strategies

Please provide specific, actionable recommendations with justifications."""

        return prompt
