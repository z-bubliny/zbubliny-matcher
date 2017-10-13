from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors


def load_model(path):
    vectors = KeyedVectors.load_word2vec_format(path, binary=False)
    model = Word2Vec()
    model.wv = vectors
    return model

