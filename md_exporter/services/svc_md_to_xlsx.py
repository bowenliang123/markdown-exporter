#!/usr/bin/env python3
"""
Markdown to XLSX conversion service
Provides common functionality for converting Markdown tables to XLSX format
"""

import os
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
from openpyxl.styles import Alignment
from openpyxl.worksheet.worksheet import Worksheet

from ..utils.markdown_utils import get_md_text
from ..utils.table_utils import SUGGESTED_SHEET_NAME, parse_md_to_tables

# A whole-cell percentage such as "12%", "-1.5%" or "1,234.5%"; group 1 captures the decimal digits
PERCENT_PATTERN = re.compile(r"^[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?%$")


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

                worksheet = writer.sheets[sheet_name]
                if not force_text:
                    _convert_percent_cells(worksheet)

                # Enable text wrapping for cells that contain line breaks
                for row in worksheet.iter_rows():
                    for cell in row:
                        if cell.value and isinstance(cell.value, str) and "\n" in cell.value:
                            cell.alignment = Alignment(wrap_text=True)

                # Auto-fit column width if supported
                if hasattr(writer.sheets[sheet_name], "autofit"):
                    writer.sheets[sheet_name].autofit(max_width=200)

        # Read temp file and write to target
        output_path.write_bytes(Path(temp_xlsx_path).read_bytes())
    finally:
        # Clean up temporary file
        os.unlink(temp_xlsx_path)


def _convert_percent_cells(worksheet: Worksheet) -> None:
    """
    Store percentage strings in data rows (e.g. "99.23%") as numbers with a percent number format,
    keeping the number of decimal places written in the source text

    Args:
        worksheet: openpyxl worksheet to convert in place
    """
    for row in worksheet.iter_rows(min_row=2):
        for cell in row:
            if not isinstance(cell.value, str):
                continue
            text = cell.value.strip()
            match = PERCENT_PATTERN.match(text)
            if not match:
                continue
            decimals = len(match.group(1) or "")
            # Round away float noise such as 99.23 / 100 == 0.9923000000000001
            cell.value = round(float(text[:-1].replace(",", "")) / 100, decimals + 2)
            cell.number_format = "0." + "0" * decimals + "%" if decimals else "0%"
