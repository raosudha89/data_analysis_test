from collections import defaultdict
from collections import OrderedDict
import numpy as np
import pdb
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from visualization import *

# Reference: https://gist.github.com/StevenMaude/ea46edc315b0f94d03b9

def tf_idf(news_contents, MAX_COUNT, topics=[], topic=None):
    contents = {}
    if topic:
        for idx in news_contents:
            if topic:
                if topic not in topics[idx]:
                    continue
            contents[idx] = news_contents[idx]
    else:
        contents = news_contents
        
    tfidf = TfidfVectorizer(lowercase=False)
    tfs = tfidf.fit_transform(contents.values())
    feature_names = tfidf.get_feature_names()
    scores = zip(feature_names, np.asarray(tfs.sum(axis=0))[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    # Write output to a file
    if topic:
        txt_outfile = open('tf_idf_%s_%d.txt' % (topic, MAX_COUNT), 'w')
    else:
        txt_outfile = open('tf_idf_%d.txt' % (MAX_COUNT), 'w')
    for w, score in sorted_scores[:MAX_COUNT]:
        txt_outfile.write('%s %f\n' % (w, score))
    txt_outfile.close()
    
    # Visualize using word cloud
    high_tf_idf_words = [w for w, v in sorted_scores[:MAX_COUNT]]
    if topic:
        word_cloud(' '.join(high_tf_idf_words), fname='tf_idf_%s_%d' % (topic, MAX_COUNT))
    else:
        word_cloud(' '.join(high_tf_idf_words), fname='tf_idf_%d'%MAX_COUNT)
    
def tf_idf_per_topic(news_contents, MAX_COUNT, topics, freq_topics):
    for topic in freq_topics:
        print topic
        tf_idf(news_contents, MAX_COUNT, topics, topic)