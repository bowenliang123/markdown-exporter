#!/usr/bin/env python3
"""
Pandoc utility functions
"""

import os
import tempfile

from md_exporter.utils import get_logger

DEFAULT_ENABLED_INPUT_EXTENSIONS = []
DEFAULT_DISABLED_INPUT_EXTENSIONS = [
    "blank_before_header",  # https://pandoc.org/MANUAL.html#extension-blank_before_header
    "space_in_atx_header",  # https://pandoc.org/MANUAL.html#extension-space_in_atx_header
]

logger = get_logger(__name__)


def pandoc_convert_file(
    source_file: str,
    input_format: str,
    dest_format: str,
    outputfile: str,
    extra_args: list[str] = None,
    enabled_input_extensions: list[str] = DEFAULT_ENABLED_INPUT_EXTENSIONS,
    disabled_input_extensions: list[str] = DEFAULT_DISABLED_INPUT_EXTENSIONS,
) -> None:
    """
    Convert file using pandoc
    """
    from pypandoc import convert_file  # noqa: PLC0415

    extra_args = extra_args or []
    enabled = enabled_input_extensions or []
    disabled = disabled_input_extensions or []

    # Build format string with extensions
    if not input_format:
        raise ValueError("input_format must be specified")
    format_w_extensions = input_format
    if enabled:
        format_w_extensions += "+" + "+".join(enabled)
    if disabled:
        format_w_extensions += "-" + "-".join(disabled)

    convert_file(
        source_file=source_file,
        format=format_w_extensions,
        to=dest_format,
        outputfile=outputfile,
        extra_args=extra_args,
    )


def _warmup_pandoc() -> None:
    """
    Warm up pandoc by converting a mock Markdown file
    This improves loading speed for subsequent pandoc operations
    """
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory(delete=True) as temp_dir:
            # Create a mock Markdown file
            input_file = os.path.join(temp_dir, "mock.md")
            output_file = os.path.join(temp_dir, "mock.docx")

            # Write minimal Markdown content
            with open(input_file, "w") as f:
                f.write("# Test\n\nThis is a test.")

            # Convert the file
            pandoc_convert_file(
                source_file=input_file, input_format="markdown", dest_format="docx", outputfile=output_file
            )

            logger.debug("Pandoc warm-up completed successfully")
    except Exception as e:
        # Log the error but don't block module import
        logger.debug(f"Pandoc warm-up failed: {e}")


# Run warm-up to speed up first conversion using pandoc
if os.environ.get("LOAD_FROM_DIFY_PLUGIN") == "1":
    _warmup_pandoc()
