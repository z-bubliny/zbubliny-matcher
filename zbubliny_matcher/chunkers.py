from nltk.tokenize import sent_tokenize
from nltk.tokenize.moses import MosesTokenizer
import iso639

class SimpleChunker:
    def chunk_words(self, sentence, language=''):
        return [word.lower() for word in sentence.strip().split()]

    def chunk_sentences(self, text, language=''):
        return [ t.strip() for t in text.strip().split(".") if t.strip() ]

class MosesChunker():
    def chunk_sentences(self, text, language='en'):
        lang = iso639.to_name(language).lower()
        try:
            sentences = sent_tokenize(text, lang)
        except LookupError:
            sentences = sent_tokenize(text)
        return sentences

    def chunk_words(self, sentence, language='en'):
        tokenizer = MosesTokenizer(lang=language)
        return tokenizer.tokenize(sentence)

