from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from md_exporter.services.svc_md_to_png import convert_md_to_png
from md_exporter.utils.file_utils import get_meta_data
from md_exporter.utils.logger_utils import get_logger
from md_exporter.utils.mimetype_utils import MimeType
from md_exporter.utils.param_utils import get_md_text_from_tool_params


class MarkdownToPngTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text_from_tool_params(tool_parameters, is_strip_wrapper=True)
        output_filename = tool_parameters.get("output_filename", "output")
        is_multi_page = tool_parameters.get("page_mode", "single") == "multi"

        try:
            with TemporaryDirectory() as temp_dir:
                temp_output_path = Path(temp_dir) / "output.png"

                # convert markdown to png using the shared function
                created_files = convert_md_to_png(md_text, temp_output_path, is_multi_page=is_multi_page)

                for i, file_path in enumerate(created_files, 1):
                    yield self.create_blob_message(
                        blob=file_path.read_bytes(),
                        meta=get_meta_data(
                            mime_type=MimeType.PNG,
                            output_filename=output_filename if len(created_files) == 1 else f"{output_filename}_{i}",
                        ),
                    )

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to PNG image")
            yield self.create_text_message(f"Failed to convert markdown text to PNG image, error: {str(e)}")
            return

        return
