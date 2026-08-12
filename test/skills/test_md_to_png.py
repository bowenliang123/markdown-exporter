import glob
import os

from test_base import TestBase


class TestMdToPng(TestBase):
    def test_md_to_png(self):
        # Single long-page PNG by default
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.png"

        self.run_script("parser/cli_md_to_png.py", input_file, output_file)

        self.verify_output_file(output_file)

    def test_md_to_png_multi_page(self):
        # Long document should produce one numbered PNG per page
        input_file = "test_output/test_md_to_png_long.md"
        output_file = "test_output/test_multi.png"

        content = "# Long Document\n\n" + ("lorem ipsum dolor sit amet " * 200 + "\n\n") * 30
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(content)
        self.register_output(input_file)

        self.run_script("parser/cli_md_to_png.py", input_file, output_file, "--multi-page")

        page_files = sorted(glob.glob("test_output/test_multi_*.png"))
        self.assertGreater(len(page_files), 1, "Multi-page PNG output was not generated")
        for page_file in page_files:
            self.assertGreater(os.path.getsize(page_file), 0, f"Output file {page_file} is empty")

    def test_md_to_png_cjk(self):
        # CJK text must render with the bundled Noto Sans CJK fonts
        input_file = "test/resources/example_md_cjk.md"
        output_file = "test_output/test_cjk.png"

        self.run_script("parser/cli_md_to_png.py", input_file, output_file)

        self.verify_output_file(output_file)
