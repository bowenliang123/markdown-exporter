#!/usr/bin/env python3
"""
Markdown to PDF conversion service
Converts Markdown to PDF via pandoc (Markdown → Typst) and typst (Typst → PDF).
"""

import re
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

from ..utils.markdown_utils import get_md_text
from ..utils.text_utils import contains_chinese, contains_japanese

# Directory containing bundled Noto Sans SC font (SIL OFL 1.1, see LICENSE there)
FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

FONT_REGULAR = "Noto Sans SC"

# Markdown image syntax: ![alt](url)
_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)\)")


def _inline_remote_images(md_text: str, work_dir: Path) -> str:
    """
    Download remote images to a sibling directory of the typst source so typst
    can resolve them at compile time. URLs that fail to download are left
    untouched (the old xhtml2pdf backend silently dropped them).
    """
    matches = _IMAGE_PATTERN.findall(md_text)
    if not matches:
        return md_text

    rewritten = md_text
    for i, (alt, url) in enumerate(matches):
        suffix = Path(urlparse(url).path).suffix or ".png"
        local_path = work_dir / f"img_{i}{suffix}"
        try:
            urllib.request.urlretrieve(url, str(local_path))  # noqa: S310
        except Exception:
            continue
        rewritten = rewritten.replace(f"![{alt}]({url})", f"![{alt}]({local_path.name})")
    return rewritten


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
    import typst  # noqa: PLC0415
    from pypandoc import convert_text  # noqa: PLC0415

    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)
    include_cjk_font = contains_chinese(processed_md) or contains_japanese(processed_md)

    # Match Microsoft Word 2013+ page defaults: A4 paper, 2.54cm top/bottom
    # and 3.17cm left/right margins. Body size follows Word's locale default
    # — 10.5pt for CJK (五号), 11pt for non-CJK. For CJK content the bundled
    # Noto Sans SC is loaded so glyphs are embedded (issue #172).
    page_setup = (
        "#set page(width: 210mm, height: 297mm, "
        "margin: (top: 2.54cm, bottom: 2.54cm, left: 3.17cm, right: 3.17cm), "
        "fill: white)\n"
    )
    if include_cjk_font:
        prelude = f'{page_setup}#set text(font: ("{FONT_REGULAR}",), size: 10.5pt, lang: "zh")\n\n'
    else:
        prelude = f"{page_setup}#set text(size: 11pt)\n\n"

    # Build the typst source in a temp directory alongside any downloaded
    # images so typst can resolve relative paths at compile time.
    with TemporaryDirectory() as work_dir:
        work_path = Path(work_dir)
        processed_md = _inline_remote_images(processed_md, work_path)
        typst_body = convert_text(source=processed_md, format="markdown", to="typst")
        typ_file_path = work_path / "doc.typ"
        typ_file_path.write_text(prelude + typst_body, encoding="utf-8")

        if include_cjk_font:
            typst.compile(
                input=str(typ_file_path),
                output=str(output_path),
                font_paths=[str(FONTS_DIR)],
            )
        else:
            typst.compile(
                input=str(typ_file_path),
                output=str(output_path),
            )
