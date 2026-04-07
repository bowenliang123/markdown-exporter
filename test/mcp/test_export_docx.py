from pathlib import Path

from markdown_exporter_mcp.tools.export_docx import handle_export_docx


def test_export_docx_creates_artifact(tmp_path: Path) -> None:
    markdown = Path("test/resources/example_md.md").read_text(encoding="utf-8")

    result = handle_export_docx(
        markdown=markdown,
        file_name="report.docx",
        options={"strip_wrapper": False, "toc": False, "template_path": None},
        artifact_root=tmp_path,
    )

    assert result.success is True
    assert result.summary
    assert len(result.artifacts) == 1

    artifact = result.artifacts[0]
    artifact_path = Path(artifact.path)

    assert artifact.name == "report.docx"
    assert artifact.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert artifact_path.exists()
    assert artifact_path.stat().st_size > 0
