#!/usr/bin/env python3
"""
Shared Typst compilation utilities
Converts Markdown to Typst via pandoc and compiles it with typst,
with CJK font support via bundled Noto Sans CJK fonts.
"""

import re
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal
from urllib.parse import urlparse

from .markdown_utils import get_md_text
from .text_utils import contains_chinese, contains_japanese_kana, contains_korean, detect_cjk_language

# Directory containing bundled Noto Sans CJK fonts (SIL OFL 1.1, see LICENSE there)
FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

# Font stacks for each CJK region. The region-specific font is listed first so
# regional glyph variants are preferred; the remaining fonts act as fallbacks.
FONTS_CJK: dict[Literal["sc", "tc", "jp", "kr"], tuple[str, ...]] = {
    "sc": ("Noto Sans CJK SC", "Noto Sans CJK TC", "Noto Sans CJK JP", "Noto Sans CJK KR"),
    "tc": ("Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans CJK KR"),
    "jp": ("Noto Sans CJK JP", "Noto Sans CJK SC", "Noto Sans CJK TC", "Noto Sans CJK KR"),
    "kr": ("Noto Sans CJK KR", "Noto Sans CJK SC", "Noto Sans CJK TC", "Noto Sans CJK JP"),
}

# Typst lang tag to use for each detected region.
LANG_MAP: dict[Literal["sc", "tc", "jp", "kr"], str] = {
    "sc": "zh",
    "tc": "zh",
    "jp": "ja",
    "kr": "ko",
}

# Match Microsoft Word 2013+ page defaults: A4 paper, 2.54cm top/bottom
# and 3.17cm left/right margins.
DEFAULT_PAGE_SETUP = (
    "#set page(width: 210mm, height: 297mm, "
    "margin: (top: 2.54cm, bottom: 2.54cm, left: 3.17cm, right: 3.17cm), "
    "fill: white)\n"
)

# Single-page setup with automatic height, producing one long page that fits
# the whole document.
SINGLE_PAGE_SETUP = (
    "#set page(width: 210mm, height: auto, "
    "margin: (top: 2.54cm, bottom: 2.54cm, left: 3.17cm, right: 3.17cm), "
    "fill: white)\n"
)

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


def _split_typst_blocks(typst_body: str) -> list[str]:
    """
    Split Typst body into logical blocks separated by blank lines.

    Respects bracket/paren/brace nesting and code fences so that multi-line
    constructs (tables, figures, code blocks) are kept intact.
    """
    blocks: list[str] = []
    current: list[str] = []
    depth = 0
    in_code_fence = False
    fence_marker: str | None = None

    for line in typst_body.splitlines():
        stripped = line.strip()

        # Handle code fences (``` or ~~~)
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_code_fence:
                # Fence starts a new block
                if current and depth == 0:
                    blocks.append("\n".join(current))
                    current = []
                in_code_fence = True
                fence_marker = marker
            elif fence_marker is not None and stripped.startswith(fence_marker):
                # Fence ends
                in_code_fence = False
                fence_marker = None
            current.append(line)
            if not in_code_fence and depth == 0:
                blocks.append("\n".join(current))
                current = []
            continue

        if in_code_fence:
            current.append(line)
            continue

        if not stripped and depth == 0:
            if current:
                blocks.append("\n".join(current))
                current = []
            continue

        current.append(line)

        # Naive nesting tracker for pandoc-generated Typst. Strings/comments are
        # ignored because they rarely contain unbalanced brackets in practice.
        for char in stripped:
            if char in "([{":
                depth += 1
            elif char in ")]}" and depth > 0:
                depth -= 1

    if current:
        blocks.append("\n".join(current))

    return blocks


def _font_setter(lang: Literal["sc", "tc", "jp", "kr"]) -> str:
    """Return a Typst `#set text(...)` directive for the given language region."""
    fonts = ", ".join(f'"{name}"' for name in FONTS_CJK[lang])
    return f'#set text(font: ({fonts}), lang: "{LANG_MAP[lang]}")\n'


def _build_cjk_source(page_setup: str, typst_body: str, doc_lang: Literal["sc", "tc", "jp", "kr"]) -> str:
    """
    Assemble the final Typst source with paragraph-level font ordering.

    The document's dominant language is used for the global `#set text`, then
    each logical block gets its own `#set text` only when the detected language
    differs from the current one.
    """
    parts = [page_setup, _font_setter(doc_lang)]
    current_lang = doc_lang

    for block in _split_typst_blocks(typst_body):
        if not block.strip():
            parts.append(block)
            continue

        block_lang = detect_cjk_language(block)
        if block_lang != current_lang:
            parts.append(_font_setter(block_lang))
            current_lang = block_lang
        parts.append(block)

    return "\n\n".join(parts)


def compile_markdown_with_typst(
    md_text: str,
    *,
    format: Literal["pdf", "png", "svg"] = "pdf",
    output_path: Path | None = None,
    page_setup: str = DEFAULT_PAGE_SETUP,
    is_strip_wrapper: bool = False,
) -> bytes | list[bytes] | None:
    """
    Compile Markdown text with typst (Markdown → Typst via pandoc, Typst → output format)

    Args:
        md_text: Markdown text to compile
        format: Output format: "pdf", "png" or "svg"
        output_path: Path to save the output file. If None, return the compiled bytes
        page_setup: Typst `#set page(...)` directive to use
        is_strip_wrapper: Whether to remove code block wrapper if present

    Returns:
        None if output_path is given, otherwise the compiled bytes
        (a list of bytes, one per page, for multi-page PNG/SVG output)

    Raises:
        ValueError: If input processing fails
        RuntimeError: If pandoc or typst conversion fails
    """
    import typst  # noqa: PLC0415
    from pypandoc import convert_text  # noqa: PLC0415

    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)
    include_cjk_font = (
        contains_chinese(processed_md) or contains_japanese_kana(processed_md) or contains_korean(processed_md)
    )

    # Build the typst source in a temp directory alongside any downloaded
    # images so typst can resolve relative paths at compile time.
    with TemporaryDirectory() as work_dir:
        work_path = Path(work_dir)
        processed_md = _inline_remote_images(processed_md, work_path)
        typst_body = convert_text(source=processed_md, format="markdown", to="typst")
        # Typst 0.13+ removed the `horizontalrule` function (renamed to `line`).
        # Pandoc 3.x still emits `#horizontalrule` for markdown thematic breaks.
        typst_body = typst_body.replace("#horizontalrule()", "#line(length: 100%)")
        typst_body = typst_body.replace("#horizontalrule", "#line(length: 100%)")

        if include_cjk_font:
            doc_lang = detect_cjk_language(processed_md)
            typst_source = _build_cjk_source(page_setup, typst_body, doc_lang)
        else:
            typst_source = f"{page_setup}#set text(size: 11pt)\n\n{typst_body}"

        typ_file_path = work_path / "doc.typ"
        typ_file_path.write_text(typst_source, encoding="utf-8")

        font_paths = [str(FONTS_DIR)] if include_cjk_font else []
        return typst.compile(
            input=str(typ_file_path),
            output=str(output_path) if output_path else None,
            font_paths=font_paths,
            format=format,
        )
