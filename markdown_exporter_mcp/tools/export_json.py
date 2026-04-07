from pathlib import Path

from mcp.server.fastmcp import FastMCP

from md_exporter.facade import export_json as export_json_files
from markdown_exporter_mcp.runtime.artifacts import build_artifact, create_job_dir, sanitize_file_name
from markdown_exporter_mcp.schemas import ExportResult, JsonOptions

JSON_MIME_TYPE = "application/json"


def handle_export_json(
    *,
    markdown: str,
    file_name: str | None = None,
    options: JsonOptions | dict | None = None,
    artifact_root: Path | None = None,
) -> ExportResult:
    if not markdown.strip():
        raise ValueError("markdown must not be empty")

    json_options = options if isinstance(options, JsonOptions) else JsonOptions.model_validate(options or {})
    final_file_name = sanitize_file_name(file_name, "table.json")
    if not final_file_name.lower().endswith(".json"):
        final_file_name = f"{final_file_name}.json"

    output_dir = create_job_dir(artifact_root)
    output_path = output_dir / final_file_name

    created_paths = export_json_files(
        markdown,
        output_path,
        style=json_options.style,
        strip_wrapper=json_options.strip_wrapper,
    )

    artifacts = [build_artifact(path, JSON_MIME_TYPE) for path in created_paths]
    return ExportResult(
        success=True,
        summary=f"Exported Markdown to JSON artifacts: {len(artifacts)} file(s)",
        artifacts=artifacts,
    )


def register_export_json(server: FastMCP) -> None:
    @server.tool(name="export_json", description="Export Markdown table content to JSON files.", structured_output=True)
    def export_json(markdown: str, file_name: str | None = None, options: dict | None = None) -> ExportResult:
        return handle_export_json(markdown=markdown, file_name=file_name, options=options)
