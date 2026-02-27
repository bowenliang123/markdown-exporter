import logging
from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

from md_exporter.services.svc_md_to_docx import convert_md_to_docx, get_default_template
from md_exporter.utils.file_utils import get_meta_data
from md_exporter.utils.mimetype_utils import MimeType
from md_exporter.utils.param_utils import get_md_text_from_tool_params


class MarkdownToDocxTool(Tool):
    logger = logging.getLogger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text_from_tool_params(tool_parameters, is_strip_wrapper=True)
        docx_template_file: File | None = tool_parameters.get("docx_template_file")
        is_enable_toc: bool = tool_parameters.get("enable_toc", "false").strip().lower() == "true"
        temp_pptx_template_file_path: str | None = None
        if docx_template_file and not isinstance(docx_template_file, File):
            raise ValueError("Not a valid file for pptx template file")

        try:
            template_path = None
            if docx_template_file:
                temp_pptx_template_file = NamedTemporaryFile(delete=False)
                temp_pptx_template_file.write(docx_template_file.blob)
                temp_pptx_template_file.close()
                temp_pptx_template_file_path = temp_pptx_template_file.name
                template_path = Path(temp_pptx_template_file_path)
            else:
                template_path = get_default_template()

            # Create temporary output file
            with NamedTemporaryFile(suffix=".docx", delete=False) as temp_output_file:
                temp_output_path = Path(temp_output_file.name)

            try:
                # Convert to DOCX using the public service
                convert_md_to_docx(
                    md_text,
                    temp_output_path,
                    template_path,
                    is_strip_wrapper=True,
                    is_enable_toc=is_enable_toc,
                )

                # Read the converted file content
                result_file_bytes = temp_output_path.read_bytes()

                yield self.create_blob_message(
                    blob=result_file_bytes,
                    meta=get_meta_data(
                        mime_type=MimeType.DOCX,
                        output_filename=tool_parameters.get("output_filename"),
                    ),
                )
            finally:
                # Clean up temporary output file
                if temp_output_path.exists():
                    temp_output_path.unlink()
        except Exception as e:
            self.logger.exception("Failed to convert markdown text to DOCX file")
            yield self.create_text_message(f"Failed to convert markdown text to DOCX file, error: {str(e)}")
            raise e
        finally:
            if temp_pptx_template_file_path:
                Path(temp_pptx_template_file_path).unlink()
