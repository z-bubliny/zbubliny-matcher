from typing import List

from .translating import translate


def naive_matcher(text, keywords, text_language, keyword_language) -> float:
    return 1.0


def simple_matcher(text: str, keywords: List[str], text_language: str, keyword_language: str) -> float:
    keywords_translated = [translate(keyword, text_language, keyword_language) for keyword in keywords]
    return sum(int(keyword in text) for keyword in keywords_translated) / len(keywords)

