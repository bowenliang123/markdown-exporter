from test_base import TestBase


class TestMdToHtml(TestBase):
    def test_md_to_html(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.html"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_html.py", input_file, output_file)

        # Verify the output file is not empty
        self.verify_output_file(output_file)

    def test_md_to_html_preserves_single_newlines(self):
        input_file = "test/resources/line_breaks_md.md"
        output_file = "test_output/test_line_breaks.html"

        self.run_script("parser/cli_md_to_html.py", input_file, output_file)
        self.verify_output_file(output_file)

        with open(output_file, encoding="utf-8") as html_file:
            html = html_file.read().lower()

        self.assertIn("<br", html)
