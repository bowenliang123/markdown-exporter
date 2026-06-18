import re

# Regex pattern for removing think tags
THINK_TAG_REGEX = re.compile(r"<think>.*?</think>", flags=re.DOTALL)

# Regex pattern for matching Chinese characters
CHINESE_CHAR_PATTERN = re.compile(r"[\u4e00-\u9fff]")

# Regex pattern for matching Japanese characters
JAPANESE_CHAR_PATTERN = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]")

# Regex pattern for matching Korean (Hangul) characters
KOREAN_CHAR_PATTERN = re.compile(
    r"[\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uAC00-\uD7AF\uD7B0-\uD7FF]"
)


def contains_chinese(text: str) -> bool:
    """Check if contains Chinese characters"""
    return bool(CHINESE_CHAR_PATTERN.search(text))


def contains_japanese(text: str) -> bool:
    """Check if contains Japanese characters"""
    return bool(JAPANESE_CHAR_PATTERN.search(text))


def contains_korean(text: str) -> bool:
    """Check if contains Korean (Hangul) characters"""
    return bool(KOREAN_CHAR_PATTERN.search(text))


def remove_think_tags(text: str) -> str:
    """Remove think tags from text"""
    return THINK_TAG_REGEX.sub("", text)


def normalize_line_breaks(text: str) -> str:
    """Normalize line breaks"""
    if "\\n" in text:
        text = text.replace("\\n", "\n")
    return text
