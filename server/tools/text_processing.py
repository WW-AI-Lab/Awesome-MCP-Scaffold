"""
文本处理工具模块

提供各种文本处理和分析功能的 MCP 工具。
"""

import re
from typing import Any

from mcp.server.fastmcp import FastMCP


def register_text_tools(mcp: FastMCP) -> None:
    """注册文本处理相关的工具"""

    @mcp.tool(title="Count Words", description="Count words in text")
    def count_words(text: str) -> dict[str, int]:
        """Count the number of words, characters, and lines in text."""
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

    @mcp.tool(title="Convert Case", description="Convert text case")
    def convert_case(text: str, case_type: str) -> str:
        """
        Convert text to different cases.
        
        Args:
            text: Input text
            case_type: Type of case conversion (upper, lower, title, capitalize)
        """
        case_type = case_type.lower()

        if case_type == "upper":
            return text.upper()
        elif case_type == "lower":
            return text.lower()
        elif case_type == "title":
            return text.title()
        elif case_type == "capitalize":
            return text.capitalize()
        else:
            raise ValueError("Invalid case_type. Use: upper, lower, title, or capitalize")

    @mcp.tool(title="Extract Emails", description="Extract email addresses from text")
    def extract_emails(text: str) -> list[str]:
        """Extract all email addresses from the given text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Remove duplicates

    @mcp.tool(title="Extract URLs", description="Extract URLs from text")
    def extract_urls(text: str) -> list[str]:
        """Extract all URLs from the given text."""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        return list(set(urls))  # Remove duplicates

    @mcp.tool(title="Replace Text", description="Replace text with regex support")
    def replace_text(text: str, pattern: str, replacement: str, use_regex: bool = False) -> str:
        """
        Replace text using simple string replacement or regex.
        
        Args:
            text: Input text
            pattern: Pattern to search for
            replacement: Replacement text
            use_regex: Whether to use regex for pattern matching
        """
        if use_regex:
            return re.sub(pattern, replacement, text)
        else:
            return text.replace(pattern, replacement)

    @mcp.tool(title="Clean Text", description="Clean and normalize text")
    def clean_text(text: str) -> str:
        """Clean text by removing extra whitespace and normalizing."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', text)
        # Strip leading/trailing whitespace
        cleaned = cleaned.strip()
        return cleaned

    @mcp.tool(title="Generate Slug", description="Generate URL-friendly slug from text")
    def generate_slug(text: str) -> str:
        """Generate a URL-friendly slug from text."""
        # Convert to lowercase
        slug = text.lower()
        # Replace spaces and special characters with hyphens
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug

    @mcp.tool(title="Text Statistics", description="Get detailed text statistics")
    def text_statistics(text: str) -> dict[str, Any]:
        """Get comprehensive statistics about the text."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Calculate average word length
        total_word_length = sum(len(word) for word in words)
        avg_word_length = total_word_length / len(words) if words else 0

        # Calculate average sentence length
        total_sentence_length = sum(len(sentence.split()) for sentence in sentences)
        avg_sentence_length = total_sentence_length / len(sentences) if sentences else 0

        return {
            "total_characters": len(text),
            "total_words": len(words),
            "total_sentences": len(sentences),
            "average_word_length": round(avg_word_length, 2),
            "average_sentence_length": round(avg_sentence_length, 2),
            "unique_words": len({word.lower() for word in words}),
            "reading_time_minutes": round(len(words) / 200, 1)  # Assuming 200 WPM
        }
