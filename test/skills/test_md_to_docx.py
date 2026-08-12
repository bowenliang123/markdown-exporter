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

    def test_md_to_docx_inherits_footer_from_template(self):
        """Regression test for GitHub issue #159:
        page-foot set in the DOCX reference template should be inherited."""
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test_with_footer.docx"
        template_file = "test/resources/docx_template_with_footer.docx"

        self.run_script("parser/cli_md_to_docx.py", input_file, output_file, "--template", template_file)
        self.verify_output_file(output_file)

        with zipfile.ZipFile(output_file, "r") as docx_zip:
            self.assertIn("word/footer1.xml", docx_zip.namelist(), "Footer was not inherited from template")
            footer_xml = docx_zip.read("word/footer1.xml").decode("utf-8")
            self.assertIn("Inherited Footer Text", footer_xml, "Template footer text was not preserved")
