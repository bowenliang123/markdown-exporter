import markdown

from .text_utils import normalize_line_breaks, remove_think_tags


def strip_markdown_wrapper(md_text: str) -> str:
    """Remove Markdown code block wrapper"""
    md_text = md_text.strip()
    wrapper = "```"
    if md_text.endswith(wrapper):
        if md_text.startswith(wrapper):
            md_text = md_text[len(wrapper) : -len(wrapper)]
        elif md_text.startswith(f"{wrapper}markdown"):
            md_text = md_text[(len(f"{wrapper}markdown")) : -len(wrapper)]
    return md_text


CSS_FOR_TABLE = """
<!-- CSS for table -->
<style>
    table, th, td {
        border: 1px solid;
    }
    table {
        width: 100%;
    }
</style>
"""


def convert_markdown_to_html(md_text: str) -> str:
    """Convert Markdown to HTML"""
    html = markdown.markdown(text=md_text, extensions=["extra", "toc"])
    return (
        f"""
    {html}
    {CSS_FOR_TABLE}
    """
        if "<table>" in html
        else html
    )


def get_md_text(
    md_text: str,
    is_strip_wrapper: bool = False,
    is_remove_think_tag: bool = True,
    is_normalize_line_breaks: bool = True,
) -> str:
    """Process Markdown text"""
    md_text = md_text.strip() if md_text else None
    if not md_text:
        raise ValueError("Empty input md_text")

    # Remove think tags
    if is_remove_think_tag:
        md_text = remove_think_tags(md_text)

    if is_strip_wrapper:
        md_text = strip_markdown_wrapper(md_text)

    # Normalize line breaks
    if is_normalize_line_breaks:
        md_text = normalize_line_breaks(md_text)

    return md_text
