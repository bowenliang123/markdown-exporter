from markdown_exporter_mcp import server as server_module


def test_parse_args_defaults_to_stdio() -> None:
    args = server_module.parse_args([])

    assert args.transport == "stdio"
    assert args.host == "127.0.0.1"
    assert args.port == 8000
    assert args.mount_path is None


def test_parse_args_supports_streamable_http() -> None:
    args = server_module.parse_args(
        ["--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8931", "--mount-path", "/mcp"]
    )

    assert args.transport == "streamable-http"
    assert args.host == "0.0.0.0"
    assert args.port == 8931
    assert args.mount_path == "/mcp"


def test_main_runs_server_with_selected_transport(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class DummyServer:
        def run(self, transport: str = "stdio", mount_path: str | None = None) -> None:
            captured["transport"] = transport
            captured["mount_path"] = mount_path

    def fake_create_server(host: str = "127.0.0.1", port: int = 8000):
        captured["host"] = host
        captured["port"] = port
        return DummyServer()

    monkeypatch.setattr(server_module, "create_server", fake_create_server)

    server_module.main(["--transport", "streamable-http", "--host", "0.0.0.0", "--port", "9000", "--mount-path", "/mcp"])

    assert captured == {
        "host": "0.0.0.0",
        "port": 9000,
        "transport": "streamable-http",
        "mount_path": "/mcp",
    }
