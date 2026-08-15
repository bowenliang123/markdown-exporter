import zipfile

from test_base import TestBase


class TestMdToDocx(TestBase):
    def test_md_to_docx(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.docx"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_docx.py", input_file, output_file)

        # Verify the output file is not empty
        self.verify_output_file(output_file)

    def test_md_to_docx_with_toc(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test_with_toc.docx"

        # Run the tool with --toc flag
        self.run_script("parser/cli_md_to_docx.py", input_file, output_file, "--toc")

        # Verify the output file is not empty
        self.verify_output_file(output_file)

    def test_md_to_docx_preserves_single_newlines(self):
        input_file = "test/resources/line_breaks_md.md"
        output_file = "test_output/test_line_breaks.docx"

        self.run_script("parser/cli_md_to_docx.py", input_file, output_file)
        self.verify_output_file(output_file)

        with zipfile.ZipFile(output_file) as docx_file:
            document_xml = docx_file.read("word/document.xml").decode("utf-8")

        self.assertIn("w:br", document_xml)
