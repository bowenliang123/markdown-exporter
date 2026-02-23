#!/usr/bin/env python3
"""
MdToPptx service
"""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from ..utils import get_logger
from ..utils.markdown_utils import get_md_text
from ..utils.pandoc_utils import pandoc_convert_file

logger = get_logger(__name__)


def get_default_template() -> Path | None:
    """
    Get the default PPTX template path

    Returns:
        Optional[Path]: Path to default template if it exists, None otherwise
    """
    script_dir = Path(__file__).resolve().parent.parent
    default_template = script_dir / "assets" / "template" / "pptx_template.pptx"
    if default_template.exists():
        return default_template
    else:
        logger.warning(f"Default PPTX template not found at {default_template}")
        return None


def convert_md_to_pptx(
    md_text: str, output_path: Path, template_path: Path | None = None, is_strip_wrapper: bool = False
) -> Path:
    """
    Convert Markdown text to PPTX format using pandoc
    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output PPTX file
        template_path: Path to PPTX template file (optional)
        is_strip_wrapper: Whether to remove code block wrapper if present
    Returns:
        Path to the created PPTX file
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

    # Convert to PPTX using pandoc

    # Prepare pandoc arguments
    extra_args = []
    if final_template_path and final_template_path.exists():
        extra_args.append(f"--reference-doc={final_template_path}")

    # Convert to PPTX - use convert_file with temporary file since convert_text doesn't work well for PPTX
    with NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as temp_md_file:
        temp_md_file.write(processed_md)
        temp_md_file_path = temp_md_file.name

    try:
        # Convert using pandoc_convert_file
        pandoc_convert_file(
            source_file=temp_md_file_path,
            input_format="markdown",
            dest_format="pptx",
            outputfile=str(output_path),
            extra_args=extra_args,
        )
        return output_path
    finally:
        # Clean up temporary file
        if os.path.exists(temp_md_file_path):
            os.unlink(temp_md_file_path)
