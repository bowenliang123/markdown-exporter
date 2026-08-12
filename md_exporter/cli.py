#!/usr/bin/env python3

import sys

# Mapping of subcommands to their module paths
SUBCOMMANDS = {
    "md_to_codeblock": "md_exporter.parser.cli_md_to_codeblock",
    "md_to_csv": "md_exporter.parser.cli_md_to_csv",
    "md_to_docx": "md_exporter.parser.cli_md_to_docx",
    "md_to_html": "md_exporter.parser.cli_md_to_html",
    "md_to_html_text": "md_exporter.parser.cli_md_to_html_text",
    "md_to_ipynb": "md_exporter.parser.cli_md_to_ipynb",
    "md_to_jira": "md_exporter.parser.cli_md_to_jira",
    "md_to_json": "md_exporter.parser.cli_md_to_json",
    "md_to_latex": "md_exporter.parser.cli_md_to_latex",
    "md_to_md": "md_exporter.parser.cli_md_to_md",
    "md_to_pdf": "md_exporter.parser.cli_md_to_pdf",
    "md_to_png": "md_exporter.parser.cli_md_to_png",
    "md_to_pptx": "md_exporter.parser.cli_md_to_pptx",
    "md_to_svg": "md_exporter.parser.cli_md_to_svg",
    "md_to_xlsx": "md_exporter.parser.cli_md_to_xlsx",
    "md_to_xml": "md_exporter.parser.cli_md_to_xml",
}


def main():
    """Main entry point for the markdown-exporter command."""
    if len(sys.argv) < 2:
        print("Error: Subcommand is required")
        print("Usage: markdown-exporter <subcommand> [options]")
        print("Subcommands:")
        for cmd in sorted(SUBCOMMANDS.keys()):
            print(f"  {cmd}")
        print("\nUse 'markdown-exporter <subcommand> --help' for help on a specific subcommand.")
        sys.exit(1)

    subcommand = sys.argv[1]

    # Handle help options
    if subcommand in ("--help", "-h"):
        print("Usage: markdown-exporter <subcommand> [options]")
        print("Subcommands:")
        for cmd in sorted(SUBCOMMANDS.keys()):
            print(f"  {cmd}")
        print("\nUse 'markdown-exporter <subcommand> --help' for help on a specific subcommand.")
        sys.exit(0)

    if subcommand not in SUBCOMMANDS:
        print(f"Error: Invalid subcommand '{subcommand}'")
        print("Usage: markdown-exporter <subcommand> [options]")
        print("Subcommands:")
        for cmd in sorted(SUBCOMMANDS.keys()):
            print(f"  {cmd}")
        print("Use 'markdown-exporter --help' for a list of all subcommands.")
        sys.exit(1)

    # Call the corresponding main function with the remaining arguments
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    try:
        # Dynamically import the module
        module_path = SUBCOMMANDS[subcommand]
        module = __import__(module_path, fromlist=["main"])
        # Get the main function
        main_func = getattr(module, "main")
        # Call the main function
        main_func()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
