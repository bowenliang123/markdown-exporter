#!/usr/bin/env python3
"""
Markdown to PDF conversion service
Converts Markdown to PDF via pandoc (Markdown → Typst) and typst (Typst → PDF).
"""

from pathlib import Path

from ..utils.typst_utils import compile_markdown_with_typst


def convert_md_to_pdf(md_text: str, output_path: Path, is_strip_wrapper: bool = False) -> None:
    """
    Convert Markdown text to PDF format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output PDF file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Raises:
        ValueError: If input processing fails
        RuntimeError: If pandoc or typst conversion fails
    """
    compile_markdown_with_typst(
        md_text,
        format="pdf",
        output_path=output_path,
        is_strip_wrapper=is_strip_wrapper,
    )
