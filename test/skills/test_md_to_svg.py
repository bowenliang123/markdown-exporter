import glob
import os

from test_base import TestBase


class TestMdToSvg(TestBase):
    def test_md_to_svg(self):
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.svg"

        self.run_script("parser/cli_md_to_svg.py", input_file, output_file)

        self.verify_output_file(output_file)

        with open(output_file, encoding="utf-8") as f:
            self.assertIn("<svg", f.read())

    def test_md_to_svg_multi_page(self):
        # Long document should produce one numbered SVG per page
        input_file = "test_output/test_md_to_svg_long.md"
        output_file = "test_output/test_svg_multi.svg"

        content = "# Long Document\n\n" + ("lorem ipsum dolor sit amet " * 200 + "\n\n") * 30
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(content)
        self.register_output(input_file)

        self.run_script("parser/cli_md_to_svg.py", input_file, output_file)

        page_files = sorted(glob.glob("test_output/test_svg_multi_*.svg"))
        self.assertGreater(len(page_files), 1, "Multi-page SVG output was not generated")
        for page_file in page_files:
            self.register_output(page_file)
            self.assertGreater(os.path.getsize(page_file), 0, f"Output file {page_file} is empty")
