from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from md_exporter.services.svc_md_to_codeblock import convert_md_to_codeblock
from md_exporter.utils.file_utils import get_meta_data
from md_exporter.utils.logger_utils import get_logger
from md_exporter.utils.mimetype_utils import MimeType
from md_exporter.utils.param_utils import get_md_text_from_tool_params, get_param_value


class MarkdownToCodeblockTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text_from_tool_params(tool_parameters)
        is_compress = get_param_value(tool_parameters, "is_compress", "true")
        compress = "true" == is_compress.lower()

        # create a temporary output path
        with NamedTemporaryFile(suffix=".zip" if compress else ".txt", delete=False) as temp_file:
            temp_output_path = Path(temp_file.name)

        try:
            # convert markdown to codeblocks using the shared function
            created_files = convert_md_to_codeblock(md_text, temp_output_path, compress=compress)

            # generate blob messages based on the created files
            if compress:
                # single ZIP file
                yield self.create_blob_message(
                    blob=created_files[0].read_bytes(),
                    meta=get_meta_data(
                        mime_type=MimeType.ZIP,
                        output_filename=tool_parameters.get("output_filename"),
                    ),
                )
            else:
                # multiple code files
                for index, file_path in enumerate(created_files):
                    # determine MIME type based on file suffix
                    suffix = file_path.suffix.lower()
                    mime_type = MimeType.TXT  # default
                    if suffix == ".css":
                        mime_type = MimeType.CSS
                    elif suffix == ".csv":
                        mime_type = MimeType.CSV
                    elif suffix == ".py":
                        mime_type = MimeType.PY
                    elif suffix == ".json":
                        mime_type = MimeType.JSON
                    elif suffix in (".js", ".javascript"):
                        mime_type = MimeType.JS
                    elif suffix in (".sh", ".bash"):
                        mime_type = MimeType.SH
                    elif suffix == ".svg":
                        mime_type = MimeType.SVG
                    elif suffix == ".xml":
                        mime_type = MimeType.XML
                    elif suffix == ".html":
                        mime_type = MimeType.HTML
                    elif suffix == ".md":
                        mime_type = MimeType.MD
                    elif suffix in (".yaml", ".yml"):
                        mime_type = MimeType.YAML
                    elif suffix == ".rb":
                        mime_type = MimeType.RUBY
                    elif suffix == ".php":
                        mime_type = MimeType.PHP
                    elif suffix == ".java":
                        mime_type = MimeType.JAVA
                    elif suffix == ".jl":
                        mime_type = MimeType.JL
                    elif suffix == ".rs":
                        mime_type = MimeType.RS

                    yield self.create_blob_message(
                        blob=file_path.read_bytes(),
                        meta=get_meta_data(
                            mime_type=mime_type,
                            output_filename=(tool_parameters.get("output_filename") or "code")
                            + (("_" + str(index + 1)) if len(created_files) > 1 else ""),
                        ),
                    )
        except Exception as e:
            self.logger.exception("Failed to convert markdown to codeblocks")
            raise e
        finally:
            # clean up temporary files
            if temp_output_path.exists():
                temp_output_path.unlink()
            # clean up any other created files if not compressed
            if not compress and "created_files" in locals():
                for file_path in created_files:
                    if file_path.exists():
                        file_path.unlink()
