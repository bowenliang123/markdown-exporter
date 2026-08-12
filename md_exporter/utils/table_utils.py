import re
from io import StringIO
from logging import Logger

import markdown
import pandas as pd
from bs4 import BeautifulSoup
from pandas.api.types import is_string_dtype

from .markdown_utils import strip_markdown_wrapper

SUGGESTED_SHEET_NAME = "suggested_sheet_name"
LINE_BREAK_PLACEHOLDER = "__MDEXPORTER_LINE_BREAK__"
BR_TAG_PATTERN = re.compile(r"<br\s*/?>", re.IGNORECASE)


def extract_headings(html_str: str, extract_headings_for_sheet_names: bool) -> list[str]:
    """Extract headings from HTML"""
    if not extract_headings_for_sheet_names:
        return []

    soup = BeautifulSoup(html_str, "html.parser")
    headings = []
    for i in range(1, 6):
        for tag in soup.find_all(f"h{i}"):
            tag_text = tag.text.strip()
            if tag_text:
                tag_text = tag_text[0:30] if len(tag_text) > 30 else tag_text
                headings.append(tag_text)
    return headings


def _replace_br_tags_with_placeholder(html_str: str) -> str:
    """Replace <br> tags with a placeholder so pandas.read_html preserves line breaks."""
    return BR_TAG_PATTERN.sub(LINE_BREAK_PLACEHOLDER, html_str)


def _restore_line_breaks(table: pd.DataFrame) -> pd.DataFrame:
    """Restore line break placeholders to actual newline characters in string columns."""
    for col in table.columns:
        if is_string_dtype(table[col]):
            table[col] = table[col].astype(str).str.replace(LINE_BREAK_PLACEHOLDER, "\n", regex=False)
    return table


def parse_md_to_tables(
    md_text: str,
    force_value_to_str: bool = True,
    extract_headings_for_sheet_names: bool = True,
    logger: Logger | None = None,
) -> list[pd.DataFrame]:
    """Parse Markdown text to tables"""
    try:
        md_text = strip_markdown_wrapper(md_text)
        if not md_text.startswith("|") and "|" in md_text:
            md_text = md_text.replace("|", "\n|", 1)

        html_str = markdown.markdown(text=md_text, extensions=["tables"])
        html_str = _replace_br_tags_with_placeholder(html_str)
        tables: list[pd.DataFrame] = pd.read_html(StringIO(html_str), encoding="utf-8")
        headings: list[str] = extract_headings(html_str, extract_headings_for_sheet_names)

        def post_process_table(table: pd.DataFrame) -> pd.DataFrame:
            table = table.fillna("")
            if force_value_to_str:
                for col in table.columns:
                    if table[col].dtype not in {"object", "string"}:
                        table[col] = table[col].astype(str)
            table = _restore_line_breaks(table)
            return table

        result_tables = []
        for i, table in enumerate(tables):
            if not table.empty:
                process_table = post_process_table(table)
                if headings and i < len(headings):
                    process_table.attrs[SUGGESTED_SHEET_NAME] = headings[i]
                result_tables.append(process_table)

        tables = result_tables

        if not tables or len(tables) <= 0:
            raise ValueError("No available tables parsed from markdown text")
        return tables
    except Exception as e:
        if logger:
            logger.exception(f"Failed to parse markdown to tables, exception: {str(e)}")
        raise ValueError(f"Failed to parse markdown to tables, exception: {str(e)}")
