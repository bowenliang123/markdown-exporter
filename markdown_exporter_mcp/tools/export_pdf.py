from pathlib import Path

from mcp.server.fastmcp import FastMCP

from md_exporter.facade import export_pdf as export_pdf_file
from markdown_exporter_mcp.runtime.artifacts import build_artifact, create_job_dir, sanitize_file_name
from markdown_exporter_mcp.schemas import ExportResult, PdfOptions

PDF_MIME_TYPE = "application/pdf"


def handle_export_pdf(
    *,
    markdown: str,
    file_name: str | None = None,
    options: PdfOptions | dict | None = None,
    artifact_root: Path | None = None,
) -> ExportResult:
    if not markdown.strip():
        raise ValueError("markdown must not be empty")

    pdf_options = options if isinstance(options, PdfOptions) else PdfOptions.model_validate(options or {})
    final_file_name = sanitize_file_name(file_name, "document.pdf")
    if not final_file_name.lower().endswith(".pdf"):
        final_file_name = f"{final_file_name}.pdf"

    output_dir = create_job_dir(artifact_root)
    output_path = output_dir / final_file_name

    export_pdf_file(markdown, output_path, strip_wrapper=pdf_options.strip_wrapper)

    artifact = build_artifact(output_path, PDF_MIME_TYPE)
    return ExportResult(
        success=True,
        summary=f"Exported Markdown to PDF: {artifact.name}",
        artifacts=[artifact],
    )


def register_export_pdf(server: FastMCP) -> None:
    @server.tool(name="export_pdf", description="Export Markdown content to a PDF document.", structured_output=True)
    def export_pdf(markdown: str, file_name: str | None = None, options: dict | None = None) -> ExportResult:
        return handle_export_pdf(markdown=markdown, file_name=file_name, options=options)
