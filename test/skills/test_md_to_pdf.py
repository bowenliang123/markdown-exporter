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
        # CJK text must use embedded Noto Sans CJK (issue #172: Adobe font pack prompt)
        input_file = "test/resources/example_md_cjk.md"
        output_file = "test_output/test_cjk.pdf"

        self.run_script("parser/cli_md_to_pdf.py", input_file, output_file)

        self.verify_output_file(output_file)

        # Embedded TrueType/CFF fonts appear as FontFile2/FontFile3 streams in the PDF
        with open(output_file, "rb") as f:
            pdf_bytes = f.read()
        has_font_stream = b"FontFile2" in pdf_bytes or b"FontFile3" in pdf_bytes
        self.assertTrue(has_font_stream, "CJK font is not embedded in the PDF")
        self.assertIn(b"NotoSansCJK", pdf_bytes, "Noto Sans CJK is not used in the PDF")

    def test_md_to_pdf_all_styles_cjk(self):
        # Exhaustive markdown style coverage across SC/TC/JP/KR, guarding against
        # regressions like PR #186 (typst 0.13+ removed `horizontalrule`).
        input_file = "test/resources/example_md_all_styles_cjk.md"
        output_file = "test_output/test_all_styles_cjk.pdf"

        self.run_script("parser/cli_md_to_pdf.py", input_file, output_file)
        self.verify_output_file(output_file)

        with open(output_file, "rb") as f:
            pdf_bytes = f.read()
        has_font_stream = b"FontFile2" in pdf_bytes or b"FontFile3" in pdf_bytes
        self.assertTrue(has_font_stream, "CJK font is not embedded in the PDF")
        self.assertIn(b"NotoSansCJKsc-Regular", pdf_bytes, "SC font is not used")
        self.assertIn(b"NotoSansCJKtc-Regular", pdf_bytes, "TC font is not used")
        self.assertIn(b"NotoSansCJKjp-Regular", pdf_bytes, "JP font is not used")
        self.assertIn(b"NotoSansCJKkr-Regular", pdf_bytes, "KR font is not used")

    def test_md_to_pdf_cjk_paragraph_level_fonts(self):
        # Mixed CJK document should use region-specific fonts per paragraph
        input_file = "test_output/mixed_cjk_input.md"
        output_file = "test_output/test_cjk_mixed.pdf"

        content = """# 多语言测试

## 简体中文

这是一个简体中文段落。

## 繁體中文

這是一段繁體中文文字。

## 日本語

これは日本語のテスト段落です。

## 한국어

이것은 한국어 테스트 문단입니다。
"""
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(content)
        self.register_output(input_file)

        self.run_script("parser/cli_md_to_pdf.py", input_file, output_file)
        self.verify_output_file(output_file)

        with open(output_file, "rb") as f:
            pdf_bytes = f.read()
        has_font_stream = b"FontFile2" in pdf_bytes or b"FontFile3" in pdf_bytes
        self.assertTrue(has_font_stream, "CJK font is not embedded in the PDF")
        self.assertIn(b"NotoSansCJKsc-Regular", pdf_bytes, "SC font is not used")
        self.assertIn(b"NotoSansCJKtc-Regular", pdf_bytes, "TC font is not used")
        self.assertIn(b"NotoSansCJKjp-Regular", pdf_bytes, "JP font is not used")
        self.assertIn(b"NotoSansCJKkr-Regular", pdf_bytes, "KR font is not used")
