from pathlib import Path

from mcp.server.fastmcp import FastMCP

from md_exporter.facade import export_html as export_html_file
from markdown_exporter_mcp.runtime.artifacts import build_artifact, create_job_dir, sanitize_file_name
from markdown_exporter_mcp.schemas import ExportResult, HtmlOptions

HTML_MIME_TYPE = "text/html"


def handle_export_html(
    *,
    markdown: str,
    file_name: str | None = None,
    options: HtmlOptions | dict | None = None,
    artifact_root: Path | None = None,
) -> ExportResult:
    if not markdown.strip():
        raise ValueError("markdown must not be empty")

    html_options = options if isinstance(options, HtmlOptions) else HtmlOptions.model_validate(options or {})
    final_file_name = sanitize_file_name(file_name, "document.html")
    if not final_file_name.lower().endswith(".html"):
        final_file_name = f"{final_file_name}.html"

    output_dir = create_job_dir(artifact_root)
    output_path = output_dir / final_file_name

    export_html_file(markdown, output_path, strip_wrapper=html_options.strip_wrapper)

    artifact = build_artifact(output_path, HTML_MIME_TYPE)
    return ExportResult(
        success=True,
        summary=f"Exported Markdown to HTML: {artifact.name}",
        artifacts=[artifact],
    )


def register_export_html(server: FastMCP) -> None:
    @server.tool(name="export_html", description="Export Markdown content to an HTML document.", structured_output=True)
    def export_html(markdown: str, file_name: str | None = None, options: dict | None = None) -> ExportResult:
        return handle_export_html(markdown=markdown, file_name=file_name, options=options)
