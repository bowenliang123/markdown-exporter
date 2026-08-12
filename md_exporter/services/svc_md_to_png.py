#!/usr/bin/env python3
"""
Markdown to PNG conversion service
Converts Markdown to PNG image(s) via pandoc (Markdown → Typst) and typst (Typst → PNG).
"""

from pathlib import Path

from ..utils.typst_utils import DEFAULT_PAGE_SETUP, SINGLE_PAGE_SETUP, compile_markdown_with_typst


def convert_md_to_png(
    md_text: str, output_path: Path, is_multi_page: bool = False, is_strip_wrapper: bool = False
) -> list[Path]:
    """
    Convert Markdown text to PNG image(s)

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output PNG file
        is_multi_page: Whether to export one PNG per A4 page (numbered files
            when the document has multiple pages). By default the whole
            document is rendered as a single long-page PNG.
        is_strip_wrapper: Whether to remove code block wrapper if present

    Returns:
        List of paths to the created PNG files

    Raises:
        ValueError: If input processing fails
        RuntimeError: If pandoc or typst conversion fails
    """
    page_setup = DEFAULT_PAGE_SETUP if is_multi_page else SINGLE_PAGE_SETUP
    result = compile_markdown_with_typst(
        md_text,
        format="png",
        page_setup=page_setup,
        is_strip_wrapper=is_strip_wrapper,
    )
    if result is None:
        raise RuntimeError("Typst compilation returned no output")
    pages = result if isinstance(result, list) else [result]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    created_files: list[Path] = []
    if len(pages) == 1:
        output_path.write_bytes(pages[0])
        created_files.append(output_path)
    else:
        for i, page_bytes in enumerate(pages, 1):
            page_file = output_path.with_name(f"{output_path.stem}_{i}.png")
            page_file.write_bytes(page_bytes)
            created_files.append(page_file)
    return created_files
