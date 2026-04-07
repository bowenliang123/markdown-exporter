from pathlib import Path

from markdown_exporter_mcp.tools.export_html import handle_export_html
from markdown_exporter_mcp.tools.export_json import handle_export_json
from markdown_exporter_mcp.tools.export_pdf import handle_export_pdf
from markdown_exporter_mcp.tools.export_pptx import handle_export_pptx
from markdown_exporter_mcp.tools.export_xlsx import handle_export_xlsx


def test_export_pdf_creates_artifact(tmp_path: Path) -> None:
    markdown = Path("test/resources/example_md.md").read_text(encoding="utf-8")

    result = handle_export_pdf(
        markdown=markdown,
        file_name="report.pdf",
        options={"strip_wrapper": False},
        artifact_root=tmp_path,
    )

    artifact = result.artifacts[0]
    artifact_path = Path(artifact.path)

    assert result.success is True
    assert artifact.name == "report.pdf"
    assert artifact.mime_type == "application/pdf"
    assert artifact_path.exists()
    assert artifact_path.stat().st_size > 0


def test_export_pptx_creates_artifact(tmp_path: Path) -> None:
    markdown = Path("test/resources/example_md_pptx.md").read_text(encoding="utf-8")

    result = handle_export_pptx(
        markdown=markdown,
        file_name="slides.pptx",
        options={"strip_wrapper": False, "template_path": None},
        artifact_root=tmp_path,
    )

    artifact = result.artifacts[0]
    artifact_path = Path(artifact.path)

    assert result.success is True
    assert artifact.name == "slides.pptx"
    assert artifact.mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    assert artifact_path.exists()
    assert artifact_path.stat().st_size > 0


def test_export_pptx_rejects_invalid_template(tmp_path: Path) -> None:
    markdown = Path("test/resources/example_md_pptx.md").read_text(encoding="utf-8")
    bad_template = tmp_path / "broken-template.pptx"
    bad_template.write_text("not a real pptx", encoding="utf-8")

    try:
        handle_export_pptx(
            markdown=markdown,
            file_name="slides.pptx",
            options={"strip_wrapper": False, "template_path": str(bad_template)},
            artifact_root=tmp_path,
        )
    except ValueError as exc:
        assert "Invalid PPTX template" in str(exc)
    else:
        raise AssertionError("Expected invalid PPTX template to be rejected")


def test_export_pptx_rejects_non_pptx_extension(tmp_path: Path) -> None:
    markdown = Path("test/resources/example_md_pptx.md").read_text(encoding="utf-8")
    wrong_extension = tmp_path / "template.zip"
    wrong_extension.write_text("not a pptx", encoding="utf-8")

    try:
        handle_export_pptx(
            markdown=markdown,
            file_name="slides.pptx",
            options={"strip_wrapper": False, "template_path": str(wrong_extension)},
            artifact_root=tmp_path,
        )
    except ValueError as exc:
        assert "expected a .pptx file" in str(exc)
    else:
        raise AssertionError("Expected non-.pptx template to be rejected")


def test_export_pptx_rejects_missing_pptx_parts(tmp_path: Path) -> None:
    import zipfile

    markdown = Path("test/resources/example_md_pptx.md").read_text(encoding="utf-8")
    incomplete_template = tmp_path / "incomplete.pptx"
    with zipfile.ZipFile(incomplete_template, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types />")

    try:
        handle_export_pptx(
            markdown=markdown,
            file_name="slides.pptx",
            options={"strip_wrapper": False, "template_path": str(incomplete_template)},
            artifact_root=tmp_path,
        )
    except ValueError as exc:
        assert "missing required PowerPoint package parts" in str(exc)
    else:
        raise AssertionError("Expected incomplete PPTX template to be rejected")


def test_export_xlsx_creates_artifact(tmp_path: Path) -> None:
    markdown = Path("test/resources/example_md_table.md").read_text(encoding="utf-8")

    result = handle_export_xlsx(
        markdown=markdown,
        file_name="table.xlsx",
        options={"strip_wrapper": False, "force_text": True},
        artifact_root=tmp_path,
    )

    artifact = result.artifacts[0]
    artifact_path = Path(artifact.path)

    assert result.success is True
    assert artifact.name == "table.xlsx"
    assert artifact.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert artifact_path.exists()
    assert artifact_path.stat().st_size > 0


def test_export_html_creates_artifact(tmp_path: Path) -> None:
    markdown = Path("test/resources/example_md.md").read_text(encoding="utf-8")

    result = handle_export_html(
        markdown=markdown,
        file_name="page.html",
        options={"strip_wrapper": False},
        artifact_root=tmp_path,
    )

    artifact = result.artifacts[0]
    artifact_path = Path(artifact.path)

    assert result.success is True
    assert artifact.name == "page.html"
    assert artifact.mime_type == "text/html"
    assert artifact_path.exists()
    assert artifact_path.read_text(encoding="utf-8")


def test_export_json_creates_artifact(tmp_path: Path) -> None:
    markdown = Path("test/resources/example_md_table.md").read_text(encoding="utf-8")

    result = handle_export_json(
        markdown=markdown,
        file_name="table.json",
        options={"strip_wrapper": False, "style": "jsonl"},
        artifact_root=tmp_path,
    )

    artifact = result.artifacts[0]
    artifact_path = Path(artifact.path)

    assert result.success is True
    assert artifact.name == "table.json"
    assert artifact.mime_type == "application/json"
    assert artifact_path.exists()
    assert artifact_path.read_text(encoding="utf-8")
