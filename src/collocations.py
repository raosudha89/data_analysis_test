from nltk.collocations import *

def collocations(token_dict):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    bigram_finder = BigramCollocationFinder.from_words(' . '.join(token_dict.values()).split())
    bigram_finder.apply_freq_filter(10)
    print bigram_finder.nbest(bigram_measures.pmi, 100)

    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    trigram_finder = TrigramCollocationFinder.from_words(' . '.join(token_dict.values()).split())
    trigram_finder.apply_freq_filter(10)
    print trigram_finder.nbest(trigram_measures.pmi, 100)