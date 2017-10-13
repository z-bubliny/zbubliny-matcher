class SimpleChunker:
    def chunk_words(self, sentence):
        return [word.lower() for word in sentence.strip().split()]

    def chunk_sentences(self, text):
        return [ t.strip() for t in text.strip().split(".") if t.strip() ]