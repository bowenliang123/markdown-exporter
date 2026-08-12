from enum import StrEnum


class MimeType(StrEnum):
    CSS = "text/css"
    CSV = "text/csv"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    EPUB = "application/epub+zip"
    HTML = "text/html"
    JS = "text/javascript"
    JAVA = "text/x-java-source"
    JL = "text/x-julia"
    JSON = "application/json"
    LATEX = "application/x-tex"
    MD = "text/markdown"
    PDF = "application/pdf"
    PHP = "application/x-httpd-php"
    PNG = "image/png"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    PY = "text/x-python"
    RS = "text/x-rust"
    RST = "text/prs.fallenstein.rst"
    RUBY = "text/x-ruby"
    TXT = "text/plain"
    SH = "application/x-sh"
    SVG = "image/svg+xml"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    XML = "text/xml"
    YAML = "text/yaml"
    ZIP = "application/zip"
    IPYNB = "application/x-ipynb+json"

    @classmethod
    def get_extension(cls, mime_type: str) -> str:
        """
        Get file extension by mime type
        :return: file extension with "." as prefix, e.g. ".txt"
        """
        mime_type_map = {
            cls.CSS: ".css",
            cls.CSV: ".csv",
            cls.EPUB: ".epub",
            cls.DOCX: ".docx",
            cls.HTML: ".html",
            cls.JS: ".js",
            cls.JAVA: ".java",
            cls.JL: ".jl",
            cls.JSON: ".json",
            cls.LATEX: ".tex",
            cls.MD: ".md",
            cls.PDF: ".pdf",
            cls.PHP: ".php",
            cls.PNG: ".png",
            cls.PPTX: ".pptx",
            cls.PY: ".py",
            cls.RS: ".rs",
            cls.RST: ".rst",
            cls.RUBY: ".rb",
            cls.TXT: ".txt",
            cls.SH: ".sh",
            cls.SVG: ".svg",
            cls.XLSX: ".xlsx",
            cls.XML: ".xml",
            cls.YAML: ".yaml",
            cls.ZIP: ".zip",
            cls.IPYNB: ".ipynb",
        }
        return mime_type_map.get(mime_type, ".bin")
