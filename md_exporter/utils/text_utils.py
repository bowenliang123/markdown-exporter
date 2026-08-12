import re
from typing import Literal

# Regex pattern for removing think tags
THINK_TAG_REGEX = re.compile(r"<think>.*?</think>", flags=re.DOTALL)

# Regex pattern for matching Chinese characters
CHINESE_CHAR_PATTERN = re.compile(r"[\u4e00-\u9fff]")

# Regex pattern for matching Japanese kana (hiragana + katakana)
JAPANESE_KANA_PATTERN = re.compile(r"[\u3040-\u309F\u30A0-\u30FF]")

# Regex pattern for matching Hangul syllables
HANGUL_PATTERN = re.compile(r"[\uAC00-\uD7AF]")

# Differential characters used to distinguish Simplified from Traditional Chinese.
# These are common characters that appear in one form but not the other.
_TRADITIONAL_SPECIFIC_CHARS = frozenset(
    "體語國學會來長門電書見東車馬魚鳥龍風義貝頁韋氣點驗觀數據網路軟體資料庫程式設計憂鬱烏龜臺灣灣門"
)
_SIMPLIFIED_SPECIFIC_CHARS = frozenset(
    "体语国学会长门电书见东车鱼鸟龙风义贝页韦气点验观数据网路软件数据库程序设计忧郁乌龟台湾湾门"
)


def contains_chinese(text: str) -> bool:
    """Check if contains Chinese characters"""
    return bool(CHINESE_CHAR_PATTERN.search(text))


def contains_japanese_kana(text: str) -> bool:
    """Check if text contains Japanese hiragana or katakana."""
    return bool(JAPANESE_KANA_PATTERN.search(text))


def contains_korean(text: str) -> bool:
    """Check if text contains Hangul syllables."""
    return bool(HANGUL_PATTERN.search(text))


def detect_cjk_language(text: str) -> Literal["sc", "tc", "jp", "kr"]:
    """
    Detect the dominant CJK language of a text fragment.

    Korean and Japanese kana are unambiguous, so they are checked first.
    For Chinese text, Simplified is returned unless Traditional-specific
    characters outnumber Simplified-specific ones.

    Args:
        text: Text to analyze.

    Returns:
        One of "sc" (Simplified Chinese), "tc" (Traditional Chinese),
        "jp" (Japanese), or "kr" (Korean).
    """
    if contains_korean(text):
        return "kr"
    if contains_japanese_kana(text):
        return "jp"

    traditional_score = sum(1 for char in text if char in _TRADITIONAL_SPECIFIC_CHARS)
    simplified_score = sum(1 for char in text if char in _SIMPLIFIED_SPECIFIC_CHARS)
    return "tc" if traditional_score > simplified_score else "sc"


def remove_think_tags(text: str) -> str:
    """Remove think tags from text"""
    return THINK_TAG_REGEX.sub("", text)


def normalize_line_breaks(text: str) -> str:
    """Normalize line breaks"""
    return text.replace("\\n", "\n")
