#!/usr/bin/env python3
"""
Markdown to DOCX conversion service
Provides common functionality for converting Markdown to DOCX format
"""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from ..utils import get_logger
from ..utils.markdown_utils import get_md_text
from ..utils.pandoc_utils import pandoc_convert_file

logger = get_logger(__name__)


def convert_md_to_docx(
    md_text: str, output_path: Path, template_path: Path | None = None, is_strip_wrapper: bool = False
) -> None:
    """
    Convert Markdown text to DOCX format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output DOCX file
        template_path: Optional path to DOCX template file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Determine template file
    final_template_path = template_path
    if not final_template_path:
        # Use default template
        final_template_path = get_default_template()

    # Prepare pandoc arguments
    extra_args = []
    if final_template_path and final_template_path.exists():
        extra_args.append(f"--reference-doc={final_template_path}")

    # Convert to DOCX - use pandoc_convert_file with temporary file since convert_text doesn't work for DOCX
    with NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as temp_md_file:
        temp_md_file.write(processed_md)
        temp_md_file_path = temp_md_file.name

    try:
        # Convert using pandoc_convert_file
        pandoc_convert_file(
            source_file=temp_md_file_path,
            input_format="markdown",
            dest_format="docx",
            outputfile=str(output_path),
            extra_args=extra_args,
        )
    finally:
        # Clean up temporary file
        os.unlink(temp_md_file_path)


def get_default_template() -> Path | None:
    """
    Get the default DOCX template path

    Returns:
        Optional[Path]: Path to default template if it exists, None otherwise
    """
    script_dir = Path(__file__).resolve().parent.parent
    default_template = script_dir.parent / "assets" / "template" / "docx_template.docx"
    if default_template.exists():
        return default_template
    else:
        logger.warning(f"Default DOCX template not found at {default_template}")
        return None
