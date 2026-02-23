#!/usr/bin/env python3
"""
Markdown to IPYNB conversion service
Provides common functionality for converting Markdown to IPYNB format
"""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from ..utils.markdown_utils import get_md_text
from ..utils.pandoc_utils import pandoc_convert_file


def _enforce_code_cells(md_text: str) -> str:
    lines = md_text.splitlines()
    processed_lines = []
    is_in_codeblock = False
    MD_CODEBLOCK_DELIMITER = "```"
    for line in lines:
        if line == MD_CODEBLOCK_DELIMITER or line.lstrip().startswith(MD_CODEBLOCK_DELIMITER):
            if not is_in_codeblock:
                processed_lines.append("```code")
                is_in_codeblock = True
            else:
                processed_lines.append(MD_CODEBLOCK_DELIMITER)
                is_in_codeblock = False
        else:
            processed_lines.append(line)
    processed_md = "\n".join(processed_lines)
    return processed_md


def convert_md_to_ipynb(md_text: str, output_path: Path, is_strip_wrapper: bool = False) -> None:
    """
    Convert Markdown text to IPYNB format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output IPYNB file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Replace code block delimiters with ```code
    # inorder to separate code cells from Markdown cells
    processed_md = _enforce_code_cells(processed_md)

    with NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as temp_md_file:
        temp_md_file.write(processed_md)
        temp_md_file_path = temp_md_file.name

    try:
        # Convert using pandoc_convert_file
        pandoc_convert_file(
            source_file=temp_md_file_path,
            input_format="markdown",
            dest_format="ipynb",
            outputfile=str(output_path),
            extra_args=[],
        )
    finally:
        # Clean up temporary file
        os.unlink(temp_md_file_path)
