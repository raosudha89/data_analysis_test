import argparse
from collections import defaultdict
from collections import OrderedDict
import csv
import gensim
from gensim import corpora
import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
import pdb
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import sys
from unidecode import unidecode

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def tf_idf(token_dict):
    tfidf = TfidfVectorizer(lowercase=False)
    tfs = tfidf.fit_transform(token_dict.values())
    feature_names = tfidf.get_feature_names()

def collocations(token_dict):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    bigram_finder = BigramCollocationFinder.from_words(' . '.join(token_dict.values()).split())
    bigram_finder.apply_freq_filter(10)
    print bigram_finder.nbest(bigram_measures.pmi, 100)

    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    trigram_finder = TrigramCollocationFinder.from_words(' . '.join(token_dict.values()).split())
    trigram_finder.apply_freq_filter(10)
    print trigram_finder.nbest(trigram_measures.pmi, 100)
    
def topic_modeling(text_data):
    NUM_TOPICS = 10
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        print(topic)
    pdb.set_trace()

def preprocess(text):
    if text == '':
        return text
    text = remove_non_ascii(text)
    #text = text.lower()
    #text = text.translate(None, string.punctuation)
    tokens = nltk.word_tokenize(text)
    #tokens = [w for w in tokens if not w in stopwords.words('english')]
    return ' '.join(tokens)

def main(args):
    lang_dict = defaultdict(int)
    headlines = defaultdict(str)
    stories = defaultdict(str)
    take_texts = defaultdict(str)
    topics = defaultdict(list)
    ct = 0
    
    with open(args.data_csv_filename) as csvfile:
        data_reader = csv.DictReader(csvfile, delimiter=',')
        for row in data_reader:
            lang = row['LANGUAGE']
            lang_dict[lang] += 1
            if lang != 'EN': #Ignoring non-english text
                continue
            if row['PRODUCTS'] == 'TEST': #Ignoring test messages
                continue
            idx = row['UNIQUE_STORY_INDEX']
            
            topics[idx] += row['TOPICS'].split()
            
            if row['EVENT_TYPE'] == 'ALERT':
                headlines[idx] = preprocess(row['HEADLINE_ALERT_TEXT'])
                stories[idx] = preprocess(row['ACCUMULATED_STORY_TEXT'])
                take_texts[idx] = preprocess(row['TAKE_TEXT'])
            elif row['EVENT_TYPE'] == 'HEADLINE':
                headlines[idx] = preprocess(row['HEADLINE_ALERT_TEXT'])
                stories[idx] = preprocess(row['ACCUMULATED_STORY_TEXT'])
                # row['TAKE_TEXT'] is always empty here
            elif row['EVENT_TYPE'] == 'STORY_TAKE_OVERWRITE':
                # row['HEADLINE_ALERT_TEXT'] can be empty when original headlines[idx] is not
                # row['ACCUMULATED_STORY_TEXT'] is always empty here
                take_texts[idx] = preprocess(row['TAKE_TEXT'])
            elif row['EVENT_TYPE'] == 'STORY_TAKE_APPEND':
                stories[idx] = preprocess(row['ACCUMULATED_STORY_TEXT'])
                take_texts[idx] = preprocess(row['TAKE_TEXT'])

            #ct += 1
            #if ct > 100000:
            #    break
    
    topic_dict = defaultdict(int)
    for idx in topics:
        topics[idx] = list(set(topics[idx]))
        for t in topics[idx]:
            topic_dict[t] += 1

    topic_dict = OrderedDict(sorted(topic_dict.items(), key=lambda x: x[1], reverse=True))
    print topic_dict
    i = 0
    freq_topics_count = 100
    for topic, ct in topic_dict.iteritems():
        if ct == len(headlines):
            continue
        i += 1
        if i > freq_topics_count:
            break
        contents = {}
        for idx in headlines:
            if topic in topics[idx]:
                contents[idx] = headlines[idx].split() + \
                                stories[idx].split() + \
                                take_texts[idx].split()
        topic_modeling(contents.values())
    
    return
    
    print len(headlines)
    collocations(headlines)
    
    contents = {}
    for idx in headlines:
        contents[idx] = headlines[idx] + ' . ' + stories[idx] + ' . ' + take_texts[idx]
        
    collocations(contents)
            
    #tf_idf(headlines)
    #tf_idf(stories)
    #tf_idf(take_texts)
            
    #print lang_dict

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--data_csv_filename", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)