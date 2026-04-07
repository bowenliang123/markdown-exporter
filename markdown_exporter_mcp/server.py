import argparse
from importlib.metadata import PackageNotFoundError, version

from mcp.server.fastmcp import FastMCP

from markdown_exporter_mcp.tools.export_docx import register_export_docx
from markdown_exporter_mcp.tools.export_html import register_export_html
from markdown_exporter_mcp.tools.export_json import register_export_json
from markdown_exporter_mcp.tools.export_pdf import register_export_pdf
from markdown_exporter_mcp.tools.export_pptx import register_export_pptx
from markdown_exporter_mcp.tools.export_xlsx import register_export_xlsx


def get_server_version() -> str:
    """Return the published package version used for MCP server metadata."""
    try:
        return version("md-exporter")
    except PackageNotFoundError:
        return "0.0.0"


def create_server(host: str = "127.0.0.1", port: int = 8000) -> FastMCP:
    """Create the markdown-exporter MCP server with the currently supported tools."""
    server = FastMCP("markdown-exporter", host=host, port=port)
    server._mcp_server.version = get_server_version()
    register_export_docx(server)
    register_export_pdf(server)
    register_export_pptx(server)
    register_export_xlsx(server)
    register_export_html(server)
    register_export_json(server)
    return server


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for local stdio or remote streamable HTTP startup."""
    parser = argparse.ArgumentParser(description="Run the markdown-exporter MCP server.")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport to use. stdio is best for local spawned clients; streamable-http is best for remote hosting.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind when using streamable-http transport.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind when using streamable-http transport.")
    parser.add_argument("--mount-path", default=None, help="Optional HTTP mount path, for example /mcp.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Run the markdown-exporter MCP server using the selected transport."""
    args = parse_args(argv)
    create_server(host=args.host, port=args.port).run(transport=args.transport, mount_path=args.mount_path)
