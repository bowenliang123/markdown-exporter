import unittest

from md_exporter.utils.text_utils import (
    contains_chinese,
    contains_japanese,
    contains_korean,
)


class TestTextUtils(unittest.TestCase):
    def test_contains_korean_hangul_syllables(self):
        self.assertTrue(contains_korean("가나다라"))

    def test_contains_korean_hangul_jamo(self):
        self.assertTrue(contains_korean("ㅁㅁㅁㅁ"))

    def test_contains_korean_mixed_with_english(self):
        self.assertTrue(contains_korean("Hello 안녕하세요"))

    def test_contains_korean_false_for_english_only(self):
        self.assertFalse(contains_korean("English only text"))

    def test_contains_korean_false_for_chinese_only(self):
        self.assertFalse(contains_korean("你好世界"))
        self.assertTrue(contains_chinese("你好世界"))

    def test_contains_korean_false_for_japanese_only(self):
        self.assertFalse(contains_korean("こんにちは"))
        self.assertTrue(contains_japanese("こんにちは"))

    def test_user_reported_sample(self):
        sample = "ㅁㅁㅁㅁ >> 가나다라"
        self.assertTrue(contains_korean(sample))


if __name__ == "__main__":
    unittest.main()
