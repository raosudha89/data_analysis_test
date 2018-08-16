import nltk
from nltk.collocations import *
from visualization import *

def bigram_collocations(token_dict, MAX_COUNT):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    bigram_finder = BigramCollocationFinder.from_words(' . '.join(token_dict.values()).split())
    bigram_finder.apply_freq_filter(10)
    high_freq_bigrams = bigram_finder.nbest(bigram_measures.pmi, MAX_COUNT)
    word_cloud(' '.join(['_'.join([w1, w2]) for (w1, w2) in high_freq_bigrams]))

def trigram_collocations(token_dict, MAX_COUNT):
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    trigram_finder = TrigramCollocationFinder.from_words(' . '.join(token_dict.values()).split())
    trigram_finder.apply_freq_filter(10)
    high_freq_trigrams = trigram_finder.nbest(trigram_measures.pmi, MAX_COUNT)
    word_cloud(' '.join(['_'.join([w1, w2, w3]) for (w1, w2, w3) in high_freq_trigrams]))