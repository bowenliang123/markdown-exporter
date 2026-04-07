from pydantic import BaseModel, Field


class Artifact(BaseModel):
    path: str
    name: str
    mime_type: str
    size: int = Field(ge=0)


class ExportResult(BaseModel):
    success: bool
    summary: str
    artifacts: list[Artifact]


class DocxOptions(BaseModel):
    strip_wrapper: bool = False
    toc: bool = False
    template_path: str | None = None


class PdfOptions(BaseModel):
    strip_wrapper: bool = False


class PptxOptions(BaseModel):
    strip_wrapper: bool = False
    template_path: str | None = None


class XlsxOptions(BaseModel):
    strip_wrapper: bool = False
    force_text: bool = True


class HtmlOptions(BaseModel):
    strip_wrapper: bool = False


class JsonOptions(BaseModel):
    strip_wrapper: bool = False
    style: str = "jsonl"
