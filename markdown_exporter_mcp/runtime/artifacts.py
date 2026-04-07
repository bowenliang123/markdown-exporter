import os
from pathlib import Path
from uuid import uuid4

from markdown_exporter_mcp.schemas import Artifact


def get_artifact_root(root: Path | None = None) -> Path:
    """Return the base directory used to store MCP-generated artifacts."""
    if root is not None:
        artifact_root = Path(root)
    else:
        local_app_data = os.getenv("LOCALAPPDATA")
        if local_app_data:
            artifact_root = Path(local_app_data) / "markdown-exporter-mcp" / "artifacts"
        else:
            artifact_root = Path.home() / ".cache" / "markdown-exporter-mcp" / "artifacts"

    artifact_root.mkdir(parents=True, exist_ok=True)
    return artifact_root


def create_job_dir(root: Path | None = None) -> Path:
    """Create an isolated output directory for one MCP tool invocation."""
    job_dir = get_artifact_root(root) / uuid4().hex
    job_dir.mkdir(parents=True, exist_ok=True)
    return job_dir


def sanitize_file_name(file_name: str | None, default_name: str) -> str:
    """Normalize a user-provided file name to a safe leaf name."""
    candidate = (file_name or default_name).strip()
    if not candidate:
        candidate = default_name
    return Path(candidate).name


def build_artifact(path: Path, mime_type: str) -> Artifact:
    """Build artifact metadata for a generated output file."""
    return Artifact(
        path=str(path.resolve()),
        name=path.name,
        mime_type=mime_type,
        size=path.stat().st_size,
    )
