#!/usr/bin/env python3
"""
Markdown to SVG converter
Converts Markdown text to SVG image(s), one SVG per page
"""

import argparse
import sys
from pathlib import Path

from ..services.svc_md_to_svg import convert_md_to_svg
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to SVG image(s)", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output SVG file path")
    parser.add_argument("--strip-wrapper", action="store_true", help="Remove code block wrapper if present")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to SVG
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_svg(md_text, output_path, args.strip_wrapper)
        for created_file in created_files:
            logger.info(f"Successfully converted to {created_file}")
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: Failed to convert to SVG - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
