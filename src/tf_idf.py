from collections import defaultdict
from collections import OrderedDict
import pdb
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from visualization import *

def tf_idf(token_dict, MAX_COUNT):
    tfidf = TfidfVectorizer(lowercase=False)
    tfs = tfidf.fit_transform(token_dict.values())
    feature_names = tfidf.get_feature_names()
    word_tfidf = defaultdict(int)
    for i in range(len(token_dict)):
        for j in tfs[i].nonzero()[1]:
            word_tfidf[feature_names[j]] = max(word_tfidf[j], tfs[i, j])
    word_tfidf = OrderedDict(sorted(word_tfidf.items(), key=lambda x: x[1], reverse=True))
    high_tf_idf_words = word_tfidf.keys()[:MAX_COUNT]
    print high_tf_idf_words
    word_cloud(' '.join(high_tf_idf_words))