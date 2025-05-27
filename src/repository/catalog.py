# cataog.py
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Catalog:
    def __init__(self):
        self._db = {}
        self.id = 0
        self.corpus = []
        self.vmodel = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=(3,5),
            lowercase=True,
            strip_accents='unicode',
            max_df=0.9,
            min_df=2
        )

    def insert(self, asset):
        asset._id = self.id
        self.corpus.append(asset._docu)
        self._db[self.id] = asset
        self.id += 1

    def get_asset(self, id):
        asset = self._db.get(id, None)
        return asset
    

    def _create_vspace(self):
        self._vspace = self.vmodel.fit_transform(self.corpus)

    def search(self, query, top_match = 10):
        matches = []

        q_vector = self.vmodel.transform([query])
        scores = cosine_similarity(self._vspace, q_vector).flatten()
        ranking = scores.argsort()[::-1]

        for i in range(top_match):
            idx = ranking[i]
            matches.append((scores[idx], self.corpus[idx], self._db[idx]))

        return matches

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as f:
            return pickle.load(f)