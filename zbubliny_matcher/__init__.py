from googletrans import Translator
from typing import List


def naive_matcher(text, keywords, text_language, keyword_language) -> float:
    return 1.0


def simple_matcher(text: str, keywords: List[str], text_language: str, keyword_language: str) -> float:
    translator = Translator()
    keywords_translated = [translator.translate(keyword, text_language, keyword_language).text for keyword in keywords]
    return [int(keyword in text) for keyword in keywords_translated] / len(keywords)