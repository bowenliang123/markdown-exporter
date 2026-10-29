#!/usr/bin/env python3
"""
Markdown to XLSX converter
Converts Markdown tables to XLSX format
"""

import argparse
import sys
from pathlib import Path

from ..services.svc_md_to_xlsx import convert_md_to_xlsx
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown tables to XLSX format", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output XLSX file path")
    parser.add_argument(
        "--force-text",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Convert cell values to text type (on by default); use --no-force-text to keep numbers as numbers",
    )
    parser.add_argument("--strip-wrapper", action="store_true", help="Remove code block wrapper if present")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to XLSX
    output_path = Path(args.output)
    try:
        convert_md_to_xlsx(md_text, output_path, args.strip_wrapper, args.force_text)
        logger.info(f"Successfully converted to {output_path}")
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: Failed to convert to XLSX - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
