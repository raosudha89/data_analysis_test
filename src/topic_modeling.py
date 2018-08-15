import gensim
from gensim import corpora
import nltk
import pdb
from visualization import *

def topic_modeling(text_data):
    NUM_TOPICS = 10
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    #pickle.dump(corpus, open('corpus.pkl', 'wb'))
    #dictionary.save('dictionary.gensim')
    #ldamodel.save('model10.gensim')
    for topic in topics:
        print(topic)
    visualize_topics(ldamodel, corpus, dictionary)
    pdb.set_trace()

def generate_interesting_words(headlines, stories, take_texts, topics=[], topic=None):
    contents = {}
    for idx in headlines:
        if topic:
            if topic not in topics[idx]:
                continue
        contents[idx] = headlines[idx].split()
    topic_modeling(contents.values())

def generate_interesting_bigram_phrases(headlines, stories, take_texts, topics=[], topic=None):
    bigram_contents = {}
    for idx in headlines:
        if topic:
            if topic not in topics[idx]:
                continue
        headline_bigrams = [' '.join([w1, w2]) for (w1, w2) in nltk.bigrams(headlines[idx].split())]
        bigram_contents[idx] = headline_bigrams
    topic_modeling(bigram_contents.values())
    
def generate_interesting_trigram_phrases(headlines, stories, take_texts, topics=[], topic=None):
    trigram_contents = {}
    for idx in headlines:
        if topic:
            if topic not in topics[idx]:
                continue
        headline_trigrams = [' '.join([w1, w2, w3]) for (w1, w2, w3) in nltk.trigrams(headlines[idx].split())]
        trigram_contents[idx] = headline_trigrams
    topic_modeling(trigram_contents.values())   