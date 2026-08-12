#!/usr/bin/env python3
"""
Markdown to SVG conversion service
Converts Markdown to SVG image(s) via pandoc (Markdown → Typst) and typst (Typst → SVG).
"""

from pathlib import Path

from ..utils.typst_utils import compile_markdown_with_typst


def convert_md_to_svg(md_text: str, output_path: Path, is_strip_wrapper: bool = False) -> list[Path]:
    """
    Convert Markdown text to SVG image(s), one SVG per page

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output SVG file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Returns:
        List of paths to the created SVG files

    Raises:
        ValueError: If input processing fails
        RuntimeError: If pandoc or typst conversion fails
    """
    result = compile_markdown_with_typst(
        md_text,
        format="svg",
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
            page_file = output_path.with_name(f"{output_path.stem}_{i}.svg")
            page_file.write_bytes(page_bytes)
            created_files.append(page_file)
    return created_files
