#!/usr/bin/env python3
"""
Markdown to Jira wiki markup converter
Converts Markdown text to Jira wiki markup and outputs to stdout
"""

import argparse
import sys

from ..services.svc_md_to_jira import convert_md_to_jira
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to Jira wiki markup and output to stdout",
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

    # Convert to Jira wiki markup
    try:
        jira_str = convert_md_to_jira(md_text)
        print(jira_str)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
