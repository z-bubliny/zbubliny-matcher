from .model_loader import load_model
import re


class SimpleWord2VecMatcher:
    def __init__(self):
        self.models = {}

    def add_language_model(self, language, model):
        self.models[language] = model

    def load_language_model(self, language, path):
        model = load_model(path)
        self.add_language_model(language, model)

    def match_keyword_text(self, model, keyword, text):
        if keyword in text:
            return 1.0
        elif keyword in model.vocab:
            pass
        else:
            return 0.0

    def __call__(text, keywords, text_language, keyword_language):
        model = self.models[text_language]
        keywords_translated = [translator.translate(keyword, text_language, keyword_language).text for keyword in keywords]