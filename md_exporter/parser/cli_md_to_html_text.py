#!/usr/bin/env python3
"""
Markdown to HTML text converter
Converts Markdown text to HTML and outputs to stdout
"""

import argparse
import sys

from ..services.svc_md_to_html_text import convert_md_to_html_text
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to HTML and output to stdout",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Input Markdown file path")

    args = parser.parse_args()

    # Read input
    input_path = args.input
    try:
        with open(input_path, encoding="utf-8") as f:
            md_text = f.read()
    except FileNotFoundError:
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)

    # Convert to HTML
    try:
        html_str = convert_md_to_html_text(md_text)
        print(html_str)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
