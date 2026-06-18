from pathlib import Path

from md_exporter.services.svc_md_to_pdf import convert_to_html_with_font_support
from pdf_test_utils import extract_pdf_text
from test_base import TestBase


class TestMdToPdf(TestBase):
    def test_md_to_pdf(self):
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.pdf"

        self.run_script("parser/cli_md_to_pdf.py", input_file, output_file)
        self.verify_output_file(output_file)

    def test_md_to_pdf_korean(self):
        input_file = "test/resources/example_md_korean_only.md"
        output_file = "test_output/test_korean.pdf"
        md_text = Path(input_file).read_text(encoding="utf-8")

        html = convert_to_html_with_font_support(md_text)
        self.assertIn("font-family", html)
        self.assertIn("HYSMyeongJo-Medium", html)
        self.assertNotIn('font-family: "Sans-serif,STSong-Light', html)

        self.run_script("parser/cli_md_to_pdf.py", input_file, output_file)
        self.verify_output_file(output_file)

        extracted_text = extract_pdf_text(output_file)
        expected_korean = ["ㅁㅁㅁㅁ", "가나다라", "안녕하세요", "한국어"]
        for text in expected_korean:
            self.assertIn(
                text,
                extracted_text,
                f"Expected Korean text {text!r} to appear in PDF output",
            )
        self.assertIn("English", extracted_text)
