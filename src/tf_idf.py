import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

def tf_idf(token_dict):
    tfidf = TfidfVectorizer(lowercase=False)
    tfs = tfidf.fit_transform(token_dict.values())
    feature_names = tfidf.get_feature_names()