from typing import List

from .chunkers import SimpleChunker
from .exceptions import LanguageNotSupported
from .translating import translate


class Word2VecMatcher:
    """Abstract base class for word2vec matchers."""
    def __init__(self, debug=False):
        self.models = {}
        self.chunker = SimpleChunker()
        self.debug = debug

    def add_language_model(self, language: str, model):
        self.models[language] = model

    def load_language_model(self, language: str, path: str):
        from .model_loader import load_model
        model = load_model(path)
        self.add_language_model(language, model)
        if self.debug:
            print("Loaded model for {0} from {1}.".format(language, path))

    def match_keyword_text(self, model, keyword: str, sentences: List[List[str]], text: str) -> float:
        if keyword in text:
            return 1.0
        elif keyword in model.wv.vocab:
            scores = [self.match_keyword_sentence(model, keyword, sentence) for sentence in sentences]
            if scores:
                return max(scores)
            else:
                return 0.0
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
        keywords_translated = [translate(keyword, text_language, keyword_language) for keyword in keywords]
        scores = [self.match_keyword_text(model, keyword, sentences, text) for keyword in keywords_translated]
        if scores:
            return max(scores)
        else:
            return 0.0


class SentenceVecMatcher(Word2VecMatcher):
    """Word2vec matcher based on whole sentences."""
    def match_keyword_sentence(self, model, keyword, sentence: List) -> float:
        if not keyword or not sentence:
            return 0.0
        result = model.wv.n_similarity([keyword], sentence)
        if self.debug:
            print("Matching {0} against {1} => {2}".format(keyword, sentence, result))
        return result


class NgramVecMatcher(Word2VecMatcher):
    """Word2vec matcher based on n-grams."""
    def __init__(self, n, debug=False):
        super(NgramVecMatcher, self).__init__(debug=debug)
        self.n = n

    def match_ngram(self, model, keyword, ngram):
        return model.wv.n_similarity([keyword], ngram)

    def match_keyword_sentence(self, model, keyword, sentence: List) -> float:
        from nltk import ngrams
        if not keyword or not sentence:
            return 0.0
        ngram_matches = [self.match_ngram(model, keyword, ngram) for ngram in ngrams(sentence, self.n)]
        if ngram_matches:
            result = max(ngram_matches)
        else:
            result = 0.0
        if self.debug:
            print("Matching {0} against {1} => {2}".format(keyword, sentence, result))
        return result