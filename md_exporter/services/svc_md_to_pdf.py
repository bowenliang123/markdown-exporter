#!/usr/bin/env python3
"""
Markdown to PDF conversion service
Provides common functionality for converting Markdown to PDF format
"""

from pathlib import Path

from ..utils.markdown_utils import convert_markdown_to_html, get_md_text
from ..utils.text_utils import contains_chinese, contains_japanese, contains_korean

_CJK_TEXT_SELECTORS = "html, body, p, h1, h2, h3, h4, h5, h6, li, ul, ol, td, th, span, div"


def _build_cjk_font_families(md_text: str) -> str:
    """Build a CSS font-family list based on scripts present in the text."""
    fonts: list[str] = []

    if contains_korean(md_text):
        fonts.extend(["HYSMyeongJo-Medium", "HYGoThic-Medium"])
    if contains_chinese(md_text):
        fonts.extend(["STSong-Light", "MSung-Light"])
    if contains_japanese(md_text):
        fonts.append("HeiseiMin-W3")

    fonts.append("sans-serif")
    return ", ".join(f'"{name}"' if name != "sans-serif" else name for name in fonts)


def convert_to_html_with_font_support(md_text: str) -> str:
    """
    Convert Markdown to HTML and add CJK font support

    Args:
        md_text: Markdown text to convert

    Returns:
        str: HTML string with appropriate font support
    """
    html_str = convert_markdown_to_html(md_text)

    if not contains_chinese(md_text) and not contains_japanese(md_text) and not contains_korean(md_text):
        return html_str

    font_families = _build_cjk_font_families(md_text)
    css_style = f"""
    <style>
        {_CJK_TEXT_SELECTORS} {{
            -pdf-word-wrap: CJK;
            font-family: {font_families};
        }}
    </style>
    """

    result = f"""
    {css_style}
    {html_str}
    """
    return result


def convert_md_to_pdf(md_text: str, output_path: Path, is_strip_wrapper: bool = False) -> None:
    """
    Convert Markdown text to PDF format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output PDF file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    from xhtml2pdf import pisa  # noqa: PLC0415

    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Convert to HTML with font support
    html_str = convert_to_html_with_font_support(processed_md)

    # Convert to PDF
    result_file_bytes = pisa.CreatePDF(
        src=html_str,
        dest_bytes=True,
        encoding="utf-8",
        capacity=400 * 1024 * 1024,
    )

    # Write to file
    output_path.write_bytes(result_file_bytes)
