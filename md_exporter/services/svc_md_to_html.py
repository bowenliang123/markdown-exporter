#!/usr/bin/env python3
"""
Markdown to HTML conversion service
Provides common functionality for converting Markdown to HTML format
"""

from pathlib import Path

from ..utils.markdown_utils import get_md_text


def convert_md_to_html(md_text: str, output_path: Path, is_strip_wrapper: bool = False) -> None:
    """
    Convert Markdown text to HTML format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output HTML file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    from pypandoc import convert_text  # noqa: PLC0415

    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Convert to HTML
    result = convert_text(processed_md, format="markdown", to="html")

    # Write to file
    output_path.write_bytes(result.encode("utf-8"))
