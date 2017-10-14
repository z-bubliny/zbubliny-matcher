import json
from googletrans import Translator
from functools import lru_cache

from .exceptions import LanguageNotSupported

ATTEMPTS = 3


@lru_cache(maxsize=4096)
def translate(word, source_language, target_language):
    try:
        for i in range(ATTEMPTS):
            try:
                translator = Translator()
                result = translator.translate(word, source_language, target_language).text
                return result.lower()
            except json.JSONDecodeError:
                pass
    except ValueError:
        raise LanguageNotSupported(
            "Google translate does not support translation from {0} to {1}.".format(source_language, target_language))