from test_base import TestBase


class TestMdToCsv(TestBase):
    def test_md_to_csv(self):
        # Define input and output paths
        input_file = "test/resources/example_md_table.md"
        output_file = "test_output/test.csv"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_csv.py", input_file, output_file)

        # Verify the output file is not empty
        self.verify_output_file(output_file)

        # Verify no BOM for ASCII-only content
        with open(output_file, "rb") as f:
            bom = f.read(3)
        self.assertNotEqual(bom, b"\xef\xbb\xbf", "ASCII-only CSV should not have UTF-8 BOM")

    def test_md_to_csv_multibyte_auto_bom(self):
        # Define input and output paths (multibyte content)
        input_file = "test/resources/example_md_table_multibyte.md"
        output_file = "test_output/test_multibyte.csv"

        # Run the tool without any encoding option
        self.run_script("parser/cli_md_to_csv.py", input_file, output_file)

        # Verify the output file is not empty
        self.verify_output_file(output_file)

        # Verify BOM (EF BB BF) is automatically added for multibyte content
        with open(output_file, "rb") as f:
            bom = f.read(3)
        self.assertEqual(bom, b"\xef\xbb\xbf", "Multibyte CSV should automatically have UTF-8 BOM")
