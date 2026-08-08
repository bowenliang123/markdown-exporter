from collections.abc import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from md_exporter.services.svc_md_to_jira import convert_md_to_jira
from md_exporter.utils.logger_utils import get_logger
from md_exporter.utils.param_utils import get_md_text_from_tool_params


class MarkdownToJiraTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text_from_tool_params(tool_parameters)

        try:
            jira_str = convert_md_to_jira(md_text, is_strip_wrapper=True)
        except Exception as e:
            self.logger.exception("Failed to convert markdown text to Jira wiki markup")
            yield self.create_text_message(f"Failed to convert markdown text to Jira wiki markup, error: {str(e)}")
            return

        yield self.create_text_message(jira_str)
        return
