#!/usr/bin/env python3
"""
Markdown to CSV conversion service
Provides common functionality for converting Markdown tables to CSV format
"""

from pathlib import Path

from ..utils.markdown_utils import get_md_text
from ..utils.table_utils import parse_md_to_tables


def convert_md_to_csv(
    md_text: str, output_path: Path = None, is_strip_wrapper: bool = False, return_strings: bool = False
) -> list[Path] | list[str]:
    """
    Convert Markdown tables to CSV format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output CSV file(s) (optional if return_strings=True)
        is_strip_wrapper: Whether to remove code block wrapper if present
        return_strings: Whether to return CSV strings instead of writing to files

    Returns:
        List[Path]: List of paths to the created CSV files if return_strings=False
        List[str]: List of CSV strings if return_strings=True

    Raises:
        ValueError: If input processing or table parsing fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Parse Markdown tables
    tables = parse_md_to_tables(processed_md)

    # Convert to CSV
    csv_strings = []
    for table in tables:
        csv_str = table.to_csv(index=False)
        csv_strings.append(csv_str)

    if return_strings:
        return csv_strings

    # Write to files
    created_files = []
    for i, csv_str in enumerate(csv_strings):
        # Determine output filename
        if len(csv_strings) > 1:
            output_file = output_path.parent / f"{output_path.stem}_{i + 1}.csv"
        else:
            output_file = output_path

        # Write to file with auto-detected encoding (BOM for multibyte content)
        output_file.write_text(csv_str, encoding=get_csv_output_encoding(csv_str))
        created_files.append(output_file)

    return created_files


def get_csv_output_encoding(csv_str: str) -> str:
    """
    Get the appropriate encoding for CSV output

    Args:
        csv_str: CSV string to check

    Returns:
        str: Encoding to use (utf-8 or utf-8-sig)
    """
    return "utf-8" if csv_str.isascii() else "utf-8-sig"
