# Markdown Exporter MCP Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a minimal Python MCP server prototype for `markdown-exporter` that exposes one working `export_docx` tool.

**Architecture:** Keep `md_exporter` as the core conversion library and add a new `markdown_exporter_mcp` package for MCP protocol glue. The first slice adds a focused facade, artifact management, a single DOCX export tool, and a test that exercises the tool handler directly without a full client round-trip.

**Tech Stack:** Python 3.11, `mcp`, `pydantic`, `pytest`, existing `md_exporter` services

---

### Task 1: Add the first failing MCP test

**Files:**
- Create: `test/mcp/test_export_docx.py`
- Test: `test/resources/example_md.md`

- [ ] **Step 1: Write the failing test**

```python
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
    assert result.artifacts[0].name == "report.docx"
    assert result.artifacts[0].path.endswith("report.docx")
    assert Path(result.artifacts[0].path).exists()
    assert Path(result.artifacts[0].path).stat().st_size > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest test/mcp/test_export_docx.py -v`
Expected: FAIL with `ModuleNotFoundError` because `markdown_exporter_mcp` does not exist yet.

### Task 2: Add the minimal shared interfaces

**Files:**
- Create: `md_exporter/facade.py`
- Create: `markdown_exporter_mcp/schemas.py`
- Create: `markdown_exporter_mcp/runtime/artifacts.py`

- [ ] **Step 1: Add a facade for DOCX export**

```python
from pathlib import Path

from .services.svc_md_to_docx import convert_md_to_docx


def export_docx(
    markdown: str,
    output_path: Path,
    *,
    template_path: Path | None = None,
    strip_wrapper: bool = False,
    toc: bool = False,
) -> None:
    convert_md_to_docx(markdown, output_path, template_path, strip_wrapper, toc)
```

- [ ] **Step 2: Add MCP result models**

```python
from pydantic import BaseModel


class Artifact(BaseModel):
    path: str
    name: str
    mime_type: str
    size: int


class ExportResult(BaseModel):
    success: bool
    summary: str
    artifacts: list[Artifact]
```

- [ ] **Step 3: Add artifact helpers**

```python
def create_job_dir(root: Path | None = None) -> Path: ...
def sanitize_file_name(file_name: str | None, default_name: str) -> str: ...
def build_artifact(path: Path, mime_type: str) -> Artifact: ...
```

### Task 3: Implement the minimal MCP package

**Files:**
- Create: `markdown_exporter_mcp/__init__.py`
- Create: `markdown_exporter_mcp/__main__.py`
- Create: `markdown_exporter_mcp/server.py`
- Create: `markdown_exporter_mcp/tools/export_docx.py`

- [ ] **Step 1: Implement the pure DOCX tool handler**

```python
def handle_export_docx(..., artifact_root: Path | None = None) -> ExportResult:
    ...
```

- [ ] **Step 2: Register the tool on a FastMCP server**

```python
def register_export_docx(server: FastMCP) -> None:
    @server.tool()
    def export_docx(...):
        return handle_export_docx(...)
```

- [ ] **Step 3: Add `create_server()` and `main()`**

```python
def create_server() -> FastMCP:
    server = FastMCP("markdown-exporter")
    register_export_docx(server)
    return server
```

### Task 4: Wire packaging and verify green

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add MCP dependencies and script entry point**

```toml
dependencies = [
    "...",
    "mcp>=1.0.0",
    "pydantic>=2.0.0",
]

[project.scripts]
markdown-exporter = "md_exporter.cli:main"
markdown-exporter-mcp = "markdown_exporter_mcp.server:main"
```

- [ ] **Step 2: Run the focused test**

Run: `uv run pytest test/mcp/test_export_docx.py -v`
Expected: PASS

- [ ] **Step 3: Run the existing DOCX CLI regression test**

Run: `uv run pytest test/skills/test_md_to_docx.py -v`
Expected: PASS
