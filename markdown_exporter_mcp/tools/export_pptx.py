from pathlib import Path
from zipfile import BadZipFile, ZipFile

from mcp.server.fastmcp import FastMCP

from md_exporter.facade import export_pptx as export_pptx_file
from markdown_exporter_mcp.runtime.artifacts import build_artifact, create_job_dir, sanitize_file_name
from markdown_exporter_mcp.schemas import ExportResult, PptxOptions

PPTX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

REQUIRED_PPTX_ENTRIES = {
    "[Content_Types].xml",
    "ppt/presentation.xml",
    "ppt/_rels/presentation.xml.rels",
}


def validate_pptx_template(template_path: Path) -> None:
    """Validate that a custom template looks like a readable PowerPoint .pptx package."""
    if not template_path.exists():
        raise ValueError(f"Invalid PPTX template: file not found: {template_path}")
    if template_path.suffix.lower() != ".pptx":
        raise ValueError(f"Invalid PPTX template: expected a .pptx file, got: {template_path.name}")

    try:
        with ZipFile(template_path) as archive:
            entry_names = set(archive.namelist())
    except BadZipFile as exc:
        raise ValueError(
            "Invalid PPTX template: the file is not a valid Office .pptx archive. "
            "Open it in Microsoft PowerPoint and save it again as a normal .pptx file."
        ) from exc

    missing_entries = sorted(REQUIRED_PPTX_ENTRIES - entry_names)
    if missing_entries:
        raise ValueError(
            "Invalid PPTX template: missing required PowerPoint package parts: " + ", ".join(missing_entries)
        )


def handle_export_pptx(
    *,
    markdown: str,
    file_name: str | None = None,
    options: PptxOptions | dict | None = None,
    artifact_root: Path | None = None,
) -> ExportResult:
    if not markdown.strip():
        raise ValueError("markdown must not be empty")

    pptx_options = options if isinstance(options, PptxOptions) else PptxOptions.model_validate(options or {})
    final_file_name = sanitize_file_name(file_name, "slides.pptx")
    if not final_file_name.lower().endswith(".pptx"):
        final_file_name = f"{final_file_name}.pptx"

    output_dir = create_job_dir(artifact_root)
    output_path = output_dir / final_file_name
    template_path = Path(pptx_options.template_path) if pptx_options.template_path else None
    if template_path is not None:
        validate_pptx_template(template_path)

    export_pptx_file(
        markdown,
        output_path,
        template_path=template_path,
        strip_wrapper=pptx_options.strip_wrapper,
    )

    artifact = build_artifact(output_path, PPTX_MIME_TYPE)
    return ExportResult(
        success=True,
        summary=f"Exported Markdown to PPTX: {artifact.name}",
        artifacts=[artifact],
    )


def register_export_pptx(server: FastMCP) -> None:
    @server.tool(name="export_pptx", description="Export Markdown content to a PPTX presentation.", structured_output=True)
    def export_pptx(markdown: str, file_name: str | None = None, options: dict | None = None) -> ExportResult:
        return handle_export_pptx(markdown=markdown, file_name=file_name, options=options)
