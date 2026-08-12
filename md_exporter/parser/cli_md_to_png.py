#!/usr/bin/env python3
"""
Markdown to PNG converter
Converts Markdown text to PNG image(s)
"""

import argparse
import sys
from pathlib import Path

from ..services.svc_md_to_png import convert_md_to_png
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to PNG image(s)", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output PNG file path")
    parser.add_argument(
        "--multi-page",
        action="store_true",
        help="Export one PNG per A4 page (numbered files) instead of a single long-page PNG",
    )
    parser.add_argument("--strip-wrapper", action="store_true", help="Remove code block wrapper if present")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to PNG
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_png(md_text, output_path, args.multi_page, args.strip_wrapper)
        for created_file in created_files:
            logger.info(f"Successfully converted to {created_file}")
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: Failed to convert to PNG - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
