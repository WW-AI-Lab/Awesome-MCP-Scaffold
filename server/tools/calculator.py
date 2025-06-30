"""
计算器工具模块

提供基础数学计算功能的 MCP 工具。
"""

import math

from mcp.server.fastmcp import FastMCP


def register_calculator_tools(mcp: FastMCP) -> None:
    """注册计算器相关的工具"""

    @mcp.tool(title="Add Numbers", description="Add two numbers together")
    def add(a: float, b: float) -> float:
        """Add two numbers and return the result."""
        return a + b

    @mcp.tool(title="Subtract Numbers", description="Subtract second number from first")
    def subtract(a: float, b: float) -> float:
        """Subtract b from a and return the result."""
        return a - b

    @mcp.tool(title="Multiply Numbers", description="Multiply two numbers")
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers and return the result."""
        return a * b

    @mcp.tool(title="Divide Numbers", description="Divide first number by second")
    def divide(a: float, b: float) -> float:
        """Divide a by b and return the result."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @mcp.tool(title="Calculate Power", description="Calculate a raised to the power of b")
    def power(a: float, b: float) -> float:
        """Calculate a raised to the power of b."""
        return a ** b

    @mcp.tool(title="Calculate Square Root", description="Calculate square root of a number")
    def sqrt(x: float) -> float:
        """Calculate the square root of x."""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)

    @mcp.tool(title="Calculate BMI", description="Calculate Body Mass Index")
    def calculate_bmi(weight_kg: float, height_m: float) -> dict:
        """
        Calculate BMI (Body Mass Index) from weight and height.
        
        Args:
            weight_kg: Weight in kilograms
            height_m: Height in meters
            
        Returns:
            Dictionary with BMI value and category
        """
        if weight_kg <= 0 or height_m <= 0:
            raise ValueError("Weight and height must be positive numbers")

        bmi = weight_kg / (height_m ** 2)

        # Determine BMI category
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        return {
            "bmi": round(bmi, 2),
            "category": category,
            "weight_kg": weight_kg,
            "height_m": height_m
        }

    @mcp.tool(title="Calculate Percentage", description="Calculate percentage of a number")
    def percentage(value: float, percentage: float) -> float:
        """Calculate percentage of a value."""
        return (value * percentage) / 100

    @mcp.tool(title="Calculate Average", description="Calculate average of a list of numbers")
    def average(numbers: list[float]) -> float:
        """Calculate the average of a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate average of empty list")
        return sum(numbers) / len(numbers)
