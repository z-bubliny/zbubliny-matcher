from .chunkers import SimpleChunker
from googletrans import Translator
from typing import List
import re


class LanguageNotSupported(RuntimeError):
    pass


class SimpleWord2VecMatcher:
    def __init__(self, debug=True):
        self.models = {}
        self.chunker = SimpleChunker()
        self.translator = Translator()
        self.debug = debug

    def add_language_model(self, language: str, model):
        self.models[language] = model

    def load_language_model(self, language: str, path: str):
        from .model_loader import load_model
        model = load_model(path)
        self.add_language_model(language, model)
        if self.debug:
            print("Loaded model for {0} from {1}.".format(language, path))

    def match_keyword_sentence(self, model, keyword, sentence: List) -> float:
        if not keyword or not sentence:
            return 0.0
        result = model.wv.n_similarity([keyword], sentence)
        if self.debug:
            print("Matching {0} against {1} => {2}".format(keyword, sentence, result))
        return result

    def match_keyword_text(self, model, keyword: str, sentences: List[List[str]], text: str) -> float:
        if keyword in text:
            return 1.0
        elif keyword in model.wv.vocab:
            return max(self.match_keyword_sentence(model, keyword, sentence) for sentence in sentences)
        else:
            return 0.0

    def __call__(self, text: str, keywords: List[str], text_language: str, keyword_language: str) -> float:
        if not self.models:
            raise LanguageNotSupported("There is no model for language: {0}, please try loading at least one model first.".format(text_language))
        model = self.models.get(text_language)
        if not model:
            raise LanguageNotSupported("There is no model for language: {0}, try one of these: {1}.".format(text_language, ", ".join(self.models.keys())))
        sentences = [
            [word for word in self.chunker.chunk_words(sentence) if word in model.wv.vocab]
            for sentence in self.chunker.chunk_sentences(text)
        ]
        try:
            keywords_translated = [self.translator.translate(keyword, text_language, keyword_language).text for keyword in keywords]
        except ValueError:
            raise LanguageNotSupported("Google translate does not support translation from {0} to {1}.".format(keyword_language, text_language))
        return max(self.match_keyword_text(model, keyword, sentences, text) for keyword in keywords_translated)
