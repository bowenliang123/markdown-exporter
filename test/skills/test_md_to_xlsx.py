from openpyxl import load_workbook
from test_base import TestBase


class TestMdToXlsx(TestBase):
    def test_md_to_xlsx_header_style(self):
        """The header row should keep the style pandas < 3.0 applied by default
        (bold, centered, thin borders), while data rows are not bold."""
        input_file = "test/resources/example_md_table.md"
        output_file = "test_output/test_header_style.xlsx"

        self.run_script("parser/cli_md_to_xlsx.py", input_file, output_file)
        self.verify_output_file(output_file)

        worksheet = load_workbook(output_file).active
        assert worksheet is not None
        for header_cell in worksheet[1]:
            self.assertTrue(header_cell.font.b, f"{header_cell.coordinate} should be bold")
            self.assertEqual(header_cell.alignment.horizontal, "center")
            self.assertEqual(header_cell.alignment.vertical, "top")
            border = header_cell.border
            for side in (border.left, border.right, border.top, border.bottom):
                self.assertEqual(side.style, "thin")
        self.assertFalse(worksheet["A2"].font.b)

    def test_md_to_xlsx_table_borders_and_header_fill(self):
        """The header row should have a light gray fill, and every data cell (including empty ones)
        should have thin borders so the sheet reads as a table."""
        input_file = "test/resources/example_md_table_with_empty_cell.md"
        output_file = "test_output/test_table_borders.xlsx"

        self.run_script("parser/cli_md_to_xlsx.py", input_file, output_file)
        self.verify_output_file(output_file)

        worksheet = load_workbook(output_file).active
        assert worksheet is not None
        for header_cell in worksheet[1]:
            self.assertEqual(header_cell.fill.fgColor.rgb, "00D9D9D9")
        for row in worksheet.iter_rows(min_row=2):
            for cell in row:
                self.assertIsNone(cell.fill.fill_type, f"{cell.coordinate} should not be filled")
                border = cell.border
                for side in (border.left, border.right, border.top, border.bottom):
                    self.assertEqual(side.style, "thin", f"{cell.coordinate} should have thin borders")
        self.assertIsNone(worksheet["B3"].value, "B3 is the empty cell in the resource")

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
