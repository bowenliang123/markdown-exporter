from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.md_to_codeblock.md_to_codeblock import MarkdownToCodeblockTool
from tools.md_to_csv.md_to_csv import MarkdownToCsvTool
from tools.md_to_docx.md_to_docx import MarkdownToDocxTool
from tools.md_to_html.md_to_html import MarkdownToHtmlTool
from tools.md_to_html_text.md_to_html_text import MarkdownToHtmlTextTool
from tools.md_to_ipynb.md_to_ipynb import MarkdownToIpynbTool
from tools.md_to_json.md_to_json import MarkdownToJsonTool
from tools.md_to_latex.md_to_latex import MarkdownToLatexTool
from tools.md_to_md.md_to_md import MarkdownToMarkdownTool
from tools.md_to_pdf.md_to_pdf import MarkdownToPdfTool
from tools.md_to_png.md_to_png import MarkdownToPngTool
from tools.md_to_pptx.md_to_pptx import MarkdownToPptxTool
from tools.md_to_svg.md_to_svg import MarkdownToSvgTool
from tools.md_to_xlsx.md_to_xlsx import MarkdownToXlsxTool
from tools.md_to_xml.md_to_xml import MarkdownToXmlTool


class MdExporterProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            tools = [
                MarkdownToCodeblockTool,
                MarkdownToCsvTool,
                MarkdownToDocxTool,
                MarkdownToHtmlTool,
                MarkdownToHtmlTextTool,
                MarkdownToJsonTool,
                MarkdownToLatexTool,
                MarkdownToMarkdownTool,
                MarkdownToPdfTool,
                MarkdownToPngTool,
                MarkdownToPptxTool,
                MarkdownToSvgTool,
                MarkdownToXlsxTool,
                MarkdownToXmlTool,
                MarkdownToIpynbTool,
            ]
            for tool in tools:
                tool.from_credentials({})
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
