import os

from test_base import TestBase


class TestMdToCodeblock(TestBase):
    def test_md_to_codeblock(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_dir = "test_output/codeblocks"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_codeblock.py", input_file, output_dir)

        # Verify the output directory is not empty
        self.verify_output_dir(output_dir)

    def test_md_to_codeblock_julia_and_rust(self):
        """Regression test for GitHub issue #168:
        Julia and Rust code blocks should be extracted with .jl and .rs suffixes."""
        input_file = "test/resources/example_md_codeblock_julia_rust.md"
        output_dir = "test_output/codeblocks_julia_rust"

        self.run_script("parser/cli_md_to_codeblock.py", input_file, output_dir)
        self.verify_output_dir(output_dir)

        created_files = sorted(os.listdir(output_dir))
        self.assertEqual(len(created_files), 2)
        self.assertTrue(any(name.endswith(".jl") for name in created_files), f"No .jl file found in {created_files}")
        self.assertTrue(any(name.endswith(".rs") for name in created_files), f"No .rs file found in {created_files}")
