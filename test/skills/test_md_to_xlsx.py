from pathlib import Path

from openpyxl import load_workbook
from test_base import TestBase

from md_exporter.services.svc_md_to_xlsx import convert_md_to_xlsx


class TestMdToXlsx(TestBase):
    def test_md_to_xlsx(self):
        # Define input and output paths
        input_file = "test/resources/example_md_table.md"
        output_file = "test_output/test.xlsx"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_xlsx.py", input_file, output_file)

        # Verify the output file is not empty
        self.verify_output_file(output_file)

    def test_md_to_xlsx_preserves_br_line_breaks(self):
        """Regression test for GitHub issues #77 and #65:
        <br> tags inside Markdown table cells should become line breaks in XLSX cells."""
        input_file = "test/resources/example_md_table_with_br.md"
        output_file = "test_output/test_br.xlsx"

        self.run_script("parser/cli_md_to_xlsx.py", input_file, output_file)
        self.verify_output_file(output_file)

        workbook = load_workbook(output_file)
        worksheet = workbook.active
        self.assertIsNotNone(worksheet, "Worksheet is empty")
        assert worksheet is not None

        # Locate the "Description" column
        description_col: int | None = None
        for col_idx, cell in enumerate(worksheet[1], start=1):
            if cell.value == "Description":
                description_col = col_idx
                break
        self.assertIsNotNone(description_col, "Description column not found")
        assert description_col is not None

        # Cell with <br> should contain a real newline and have wrap text enabled
        item_1_description = worksheet.cell(row=2, column=description_col)
        self.assertEqual(item_1_description.value, "Line one\nLine two")
        self.assertTrue(item_1_description.alignment.wrap_text)

        # Regular cell should not contain a newline
        item_2_description = worksheet.cell(row=3, column=description_col)
        self.assertEqual(item_2_description.value, "Single line")

    def test_md_to_xlsx_percent_values_in_numeric_mode(self):
        """With force_text disabled, percentage strings should become numbers with a percent format
        that keeps the source decimal places; other text and the header stay as they are."""
        input_file = Path("test/resources/example_md_table_percent.md")
        output_file = Path("test_output/test_percent_numeric.xlsx")
        self.register_output(str(output_file))

        convert_md_to_xlsx(input_file.read_text(encoding="utf-8"), output_file, force_text=False)
        self.verify_output_file(str(output_file))

        worksheet = load_workbook(output_file).active
        assert worksheet is not None
        expected = {"B2": (0.9923, "0.00%"), "B3": (-0.015, "0.0%"), "B4": (12.345, "0.0%"), "B5": (0.5, "0%")}
        for coordinate, (value, number_format) in expected.items():
            self.assertEqual(worksheet[coordinate].value, value, coordinate)
            self.assertEqual(worksheet[coordinate].number_format, number_format, coordinate)
        # Text that merely contains a percentage is not converted
        self.assertEqual(worksheet["C2"].value, "Target: 99% or more")
        self.assertEqual(worksheet["C3"].value, "12 %")
        self.assertEqual(worksheet["C5"].value, "50%+")
        self.assertEqual(worksheet["B1"].value, "Rate")

    def test_md_to_xlsx_percent_values_stay_text_by_default(self):
        """With the default force_text mode, percentages are kept as text."""
        input_file = "test/resources/example_md_table_percent.md"
        output_file = "test_output/test_percent_text.xlsx"

        self.run_script("parser/cli_md_to_xlsx.py", input_file, output_file)
        self.verify_output_file(output_file)

        worksheet = load_workbook(output_file).active
        assert worksheet is not None
        self.assertEqual(worksheet["B2"].value, "99.23%")
        self.assertEqual(worksheet["B2"].number_format, "General")
