#!/usr/bin/env python3
"""
Markdown to XLSX conversion service
Provides common functionality for converting Markdown tables to XLSX format
"""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd

from ..utils.markdown_utils import get_md_text
from ..utils.table_utils import SUGGESTED_SHEET_NAME, parse_md_to_tables


def convert_md_to_xlsx(
    md_text: str, output_path: Path, is_strip_wrapper: bool = False, force_text: bool = True
) -> None:
    """
    Convert Markdown tables to XLSX format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output XLSX file
        is_strip_wrapper: Whether to remove code block wrapper if present
        force_text: Whether to convert cell values to text type

    Raises:
        ValueError: If input processing or table parsing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Parse Markdown tables
    tables = parse_md_to_tables(processed_md, force_value_to_str=force_text)

    # Convert to XLSX
    with NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_xlsx_file:
        temp_xlsx_path = temp_xlsx_file.name

    try:
        with pd.ExcelWriter(temp_xlsx_path, engine="openpyxl") as writer:
            for i, table in enumerate(tables):
                sheet_name = table.attrs.get(SUGGESTED_SHEET_NAME, f"Sheet{i + 1}")
                table.to_excel(writer, sheet_name=sheet_name, index=False, na_rep="")
                # Auto-fit column width if supported
                if hasattr(writer.sheets[sheet_name], "autofit"):
                    writer.sheets[sheet_name].autofit(max_width=200)

        # Read temp file and write to target
        output_path.write_bytes(Path(temp_xlsx_path).read_bytes())
    finally:
        # Clean up temporary file
        os.unlink(temp_xlsx_path)
