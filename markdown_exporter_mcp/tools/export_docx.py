from pathlib import Path

from mcp.server.fastmcp import FastMCP

from md_exporter.facade import export_docx as export_docx_file
from markdown_exporter_mcp.runtime.artifacts import build_artifact, create_job_dir, sanitize_file_name
from markdown_exporter_mcp.schemas import DocxOptions, ExportResult

DOCX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def handle_export_docx(
    *,
    markdown: str,
    file_name: str | None = None,
    options: DocxOptions | dict | None = None,
    artifact_root: Path | None = None,
) -> ExportResult:
    """Export Markdown text into a DOCX artifact and return structured metadata."""
    if not markdown.strip():
        raise ValueError("markdown must not be empty")

    docx_options = options if isinstance(options, DocxOptions) else DocxOptions.model_validate(options or {})
    final_file_name = sanitize_file_name(file_name, "document.docx")
    if not final_file_name.lower().endswith(".docx"):
        final_file_name = f"{final_file_name}.docx"

    output_dir = create_job_dir(artifact_root)
    output_path = output_dir / final_file_name
    template_path = Path(docx_options.template_path) if docx_options.template_path else None

    export_docx_file(
        markdown,
        output_path,
        template_path=template_path,
        strip_wrapper=docx_options.strip_wrapper,
        toc=docx_options.toc,
    )

    artifact = build_artifact(output_path, DOCX_MIME_TYPE)
    return ExportResult(
        success=True,
        summary=f"Exported Markdown to DOCX: {artifact.name}",
        artifacts=[artifact],
    )


def register_export_docx(server: FastMCP) -> None:
    """Register the DOCX export tool on the provided MCP server."""

    @server.tool(name="export_docx", description="Export Markdown content to a DOCX document.", structured_output=True)
    def export_docx(markdown: str, file_name: str | None = None, options: dict | None = None) -> ExportResult:
        return handle_export_docx(markdown=markdown, file_name=file_name, options=options)
