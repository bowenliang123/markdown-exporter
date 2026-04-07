from pathlib import Path

from .services.svc_md_to_docx import convert_md_to_docx
from .services.svc_md_to_html import convert_md_to_html
from .services.svc_md_to_json import convert_md_to_json
from .services.svc_md_to_pdf import convert_md_to_pdf
from .services.svc_md_to_pptx import convert_md_to_pptx
from .services.svc_md_to_xlsx import convert_md_to_xlsx


def export_docx(
    markdown: str,
    output_path: Path,
    *,
    template_path: Path | None = None,
    strip_wrapper: bool = False,
    toc: bool = False,
) -> None:
    """Export Markdown content to a DOCX file using the shared service layer."""
    convert_md_to_docx(markdown, output_path, template_path, strip_wrapper, toc)


def export_pdf(markdown: str, output_path: Path, *, strip_wrapper: bool = False) -> None:
    """Export Markdown content to a PDF file using the shared service layer."""
    convert_md_to_pdf(markdown, output_path, strip_wrapper)


def export_pptx(
    markdown: str,
    output_path: Path,
    *,
    template_path: Path | None = None,
    strip_wrapper: bool = False,
) -> Path:
    """Export Markdown content to a PPTX file using the shared service layer."""
    return convert_md_to_pptx(markdown, output_path, template_path, strip_wrapper)


def export_xlsx(markdown: str, output_path: Path, *, strip_wrapper: bool = False, force_text: bool = True) -> None:
    """Export Markdown table content to an XLSX file using the shared service layer."""
    convert_md_to_xlsx(markdown, output_path, strip_wrapper, force_text)


def export_html(markdown: str, output_path: Path, *, strip_wrapper: bool = False) -> None:
    """Export Markdown content to an HTML file using the shared service layer."""
    convert_md_to_html(markdown, output_path, strip_wrapper)


def export_json(
    markdown: str,
    output_path: Path,
    *,
    style: str = "jsonl",
    strip_wrapper: bool = False,
) -> list[Path]:
    """Export Markdown table content to JSON files using the shared service layer."""
    return convert_md_to_json(markdown, output_path, style, strip_wrapper)
