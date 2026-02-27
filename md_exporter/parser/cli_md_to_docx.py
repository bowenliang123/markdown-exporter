#!/usr/bin/env python3
"""
Markdown to DOCX converter
Converts Markdown text to DOCX format
"""

import argparse
import sys
from pathlib import Path

from ..services.svc_md_to_docx import convert_md_to_docx
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to DOCX format", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output DOCX file path")
    parser.add_argument("--template", help="Path to DOCX template file (optional)")
    parser.add_argument("--strip-wrapper", action="store_true", help="Remove code block wrapper if present")
    parser.add_argument("--toc", action="store_true", help="Include table of contents in the output")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Determine template file
    template_path = None
    if args.template:
        template_path = Path(args.template)
        if not template_path.exists():
            logger.error(f"Error: Template file not found: {args.template}")
            sys.exit(1)

    # Convert to DOCX
    output_path = Path(args.output)
    try:
        convert_md_to_docx(md_text, output_path, template_path, args.strip_wrapper, args.toc)
        logger.info(f"Successfully converted to {output_path}")
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: Failed to convert to DOCX - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
