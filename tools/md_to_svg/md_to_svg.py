from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from md_exporter.services.svc_md_to_svg import convert_md_to_svg
from md_exporter.utils.file_utils import get_meta_data
from md_exporter.utils.logger_utils import get_logger
from md_exporter.utils.mimetype_utils import MimeType
from md_exporter.utils.param_utils import get_md_text_from_tool_params


class MarkdownToSvgTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text_from_tool_params(tool_parameters, is_strip_wrapper=True)
        output_filename = tool_parameters.get("output_filename", "output")

        try:
            with TemporaryDirectory() as temp_dir:
                temp_output_path = Path(temp_dir) / "output.svg"

                # convert markdown to svg using the shared function
                created_files = convert_md_to_svg(md_text, temp_output_path)

                for i, file_path in enumerate(created_files, 1):
                    yield self.create_blob_message(
                        blob=file_path.read_bytes(),
                        meta=get_meta_data(
                            mime_type=MimeType.SVG,
                            output_filename=output_filename if len(created_files) == 1 else f"{output_filename}_{i}",
                        ),
                    )

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to SVG image")
            yield self.create_text_message(f"Failed to convert markdown text to SVG image, error: {str(e)}")
            return

        return
