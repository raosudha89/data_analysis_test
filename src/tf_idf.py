from collections import defaultdict
from collections import OrderedDict
import numpy as np
import pdb
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from visualization import *

# Reference: https://gist.github.com/StevenMaude/ea46edc315b0f94d03b9

def tf_idf(news_contents, MAX_COUNT, topics=[], topic=None):
    if topic:
        contents = {}
        for idx in news_contents:
            if topic:
                if topic not in topics[idx]:
                    continue
            contents[idx] = news_contents[idx].split()
    else:
        contents = news_contents
        
    tfidf = TfidfVectorizer(lowercase=False)
    tfs = tfidf.fit_transform(contents.values())
    feature_names = tfidf.get_feature_names()
    scores = zip(feature_names, np.asarray(tfs.sum(axis=0))[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    print sorted_scores[:MAX_COUNT]
    high_tf_idf_words = [w for w, v in sorted_scores[:MAX_COUNT]]
    word_cloud(' '.join(high_tf_idf_words), fname='tf_idf_%d'%MAX_COUNT)
    
def tf_idf_per_topic(news_contents, MAX_COUNT, topics, freq_topics):
    for topic in freq_topics:
        print topic
        tf_idf(news_contents, MAX_COUNT, topics, topic)