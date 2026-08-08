#!/usr/bin/env python3
"""
MdToJira service
"""

from pypandoc import convert_text

from ..utils.markdown_utils import get_md_text


def convert_md_to_jira(md_text: str, is_strip_wrapper: bool = False) -> str:
    """
    Convert Markdown text to Jira wiki markup format
    Args:
        md_text: Markdown text to convert
        is_strip_wrapper: Whether to remove code block wrapper if present
    Returns:
        Jira wiki markup formatted string
    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Convert to Jira wiki markup
    try:
        jira_str = convert_text(processed_md, format="markdown", to="jira")
        return jira_str
    except Exception as e:
        raise Exception(f"Failed to convert Markdown to Jira wiki markup: {e}")
