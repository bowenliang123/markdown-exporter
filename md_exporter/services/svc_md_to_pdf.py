#!/usr/bin/env python3
"""
Markdown to PDF conversion service
Provides common functionality for converting Markdown to PDF format
"""

from pathlib import Path

from ..utils.markdown_utils import convert_markdown_to_html, get_md_text
from ..utils.text_utils import contains_chinese, contains_japanese

# Directory containing bundled Noto Sans SC fonts (SIL OFL 1.1, see LICENSE there)
FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

FONT_REGULAR = "NotoSansSC-Regular.ttf"


def convert_to_html_with_font_support(md_text: str) -> str:
    """
    Convert Markdown to HTML and add Chinese/Japanese font support

    Args:
        md_text: Markdown text to convert

    Returns:
        str: HTML string with appropriate font support
    """
    html_str = convert_markdown_to_html(md_text)

    if not contains_chinese(md_text) and not contains_japanese(md_text):
        return html_str

    # Embed bundled Noto Sans SC so generated PDFs carry real glyph data
    # (Adobe's standard CID font names like STSong-Light are references only
    # and require viewers to install an Asian language font pack)
    css_style = f"""
    <style>
        @font-face {{
            font-family: NotoSansSC;
            src: url({FONT_REGULAR});
        }}
        html {{
            -pdf-word-wrap: CJK;
            font-family: NotoSansSC;
        }}
    </style>
    """

    result = f"""
    {css_style}
    {html_str}
    """
    return result


def _font_link_callback(uri: str, rel: str) -> str:
    """
    Resolve @font-face relative URLs to bundled font file paths.

    xhtml2pdf cannot handle file:// absolute URLs in @font-face, so font
    files are referenced by bare file name and resolved here. Other
    resources are left untouched.
    """
    font_path = FONTS_DIR / Path(uri).name
    if font_path.name == FONT_REGULAR and font_path.exists():
        return str(font_path)
    return uri


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
        link_callback=_font_link_callback,
    )

    # Write to file
    output_path.write_bytes(result_file_bytes)
