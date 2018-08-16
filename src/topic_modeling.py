import gensim
from gensim import corpora
import nltk
import pdb
from visualization import *

# Reference: https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21

def lda(text_data, out_fname, NUM_TOPICS=10):
    dictionary = corpora.Dictionary(text_data)
    dictionary.filter_extremes(no_below=100, no_above=0.5, keep_n=10000)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=2)
    topics = ldamodel.print_topics(num_words=30)
    for num, topic in enumerate(topics):
        word_probs = []
        word_probs_str = topic[1:][0].split(' + ')
        for i in range(len(word_probs_str)):
            word = str(word_probs_str[i].split('*')[1].strip('"'))
            prob = float(word_probs_str[i].split('*')[0])
            word_probs.append((word, prob))
        print 'Topic: %d' % num
        print(word_probs)
    visualize_topics(ldamodel, corpus, dictionary, out_fname)

def generate_interesting_words(news_contents, topics=[], topic=None):
    contents = {}
    for idx in news_contents:
        if topic:
            if topic not in topics[idx]:
                continue
        contents[idx] = news_contents[idx].split()
    lda(contents.values(), out_fname="topic_modeling_words")

def generate_interesting_bigram_phrases(news_contents, topics=[], topic=None):
    bigram_contents = {}
    for idx in news_contents:
        if topic:
            if topic not in topics[idx]:
                continue
        news_content_bigrams = [' '.join([w1, w2]) for (w1, w2) in nltk.bigrams(news_contents[idx].split())]
        bigram_contents[idx] = news_content_bigrams
    lda(bigram_contents.values(), out_fname="topic_modeling_bigrams")
    
def generate_interesting_trigram_phrases(news_contents, topics=[], topic=None):
    trigram_contents = {}
    for idx in news_contents:
        if topic:
            if topic not in topics[idx]:
                continue
        news_content_trigrams = [' '.join([w1, w2, w3]) for (w1, w2, w3) in nltk.trigrams(news_contents[idx].split())]
        trigram_contents[idx] = news_content_trigrams
    lda(trigram_contents.values(), out_fname="topic_modeling_trigrams")

def topic_modeling(news_contents):
    start_time = time.time()
    print 'Finding interesting words using topic modeling'
    generate_interesting_words(news_contents)
    print 'Done! Time taken ', time.time() - start_time
    print
    start_time = time.time()
    print 'Finding interesting bigram phrases using topic modeling'
    generate_interesting_bigram_phrases(news_contents)
    print 'Done! Time taken ', time.time() - start_time
    print
    start_time = time.time()
    print 'Finding interesting trigram phrases using topic modeling'
    generate_interesting_trigram_phrases(news_contents)
    print 'Done! Time taken ', time.time() - start_time
    print

def topic_modeling_per_topic(news_contents, topics, freq_topics):
    for topic in freq_topics:
        print topic
        generate_interesting_words(news_contents)
        generate_interesting_bigram_phrases(news_contents, topics, topic)
        generate_interesting_trigram_phrases(news_contents, topics, topic)
        
        