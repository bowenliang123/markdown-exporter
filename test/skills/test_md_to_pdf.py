from test_base import TestBase


class TestMdToPdf(TestBase):
    def test_md_to_pdf(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.pdf"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_pdf.py", input_file, output_file)

        # Verify the output file is not empty
        self.verify_output_file(output_file)

    def test_md_to_pdf_cjk_embeds_font(self):
        # CJK text must use embedded Noto Sans SC (issue #172: Adobe font pack prompt)
        input_file = "test/resources/example_md_cjk.md"
        output_file = "test_output/test_cjk.pdf"

        self.run_script("parser/cli_md_to_pdf.py", input_file, output_file)

        self.verify_output_file(output_file)

        # Embedded TrueType fonts appear as FontFile2 streams in the PDF
        with open(output_file, "rb") as f:
            pdf_bytes = f.read()
        self.assertIn(b"FontFile2", pdf_bytes, "CJK font is not embedded in the PDF")
        self.assertIn(b"NotoSansSC", pdf_bytes, "Noto Sans SC is not used in the PDF")
