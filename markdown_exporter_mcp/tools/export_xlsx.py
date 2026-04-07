from pathlib import Path

from mcp.server.fastmcp import FastMCP

from md_exporter.facade import export_xlsx as export_xlsx_file
from markdown_exporter_mcp.runtime.artifacts import build_artifact, create_job_dir, sanitize_file_name
from markdown_exporter_mcp.schemas import ExportResult, XlsxOptions

XLSX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def handle_export_xlsx(
    *,
    markdown: str,
    file_name: str | None = None,
    options: XlsxOptions | dict | None = None,
    artifact_root: Path | None = None,
) -> ExportResult:
    if not markdown.strip():
        raise ValueError("markdown must not be empty")

    xlsx_options = options if isinstance(options, XlsxOptions) else XlsxOptions.model_validate(options or {})
    final_file_name = sanitize_file_name(file_name, "table.xlsx")
    if not final_file_name.lower().endswith(".xlsx"):
        final_file_name = f"{final_file_name}.xlsx"

    output_dir = create_job_dir(artifact_root)
    output_path = output_dir / final_file_name

    export_xlsx_file(
        markdown,
        output_path,
        strip_wrapper=xlsx_options.strip_wrapper,
        force_text=xlsx_options.force_text,
    )

    artifact = build_artifact(output_path, XLSX_MIME_TYPE)
    return ExportResult(
        success=True,
        summary=f"Exported Markdown to XLSX: {artifact.name}",
        artifacts=[artifact],
    )


def register_export_xlsx(server: FastMCP) -> None:
    @server.tool(name="export_xlsx", description="Export Markdown table content to an XLSX workbook.", structured_output=True)
    def export_xlsx(markdown: str, file_name: str | None = None, options: dict | None = None) -> ExportResult:
        return handle_export_xlsx(markdown=markdown, file_name=file_name, options=options)
