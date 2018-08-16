import argparse
from collocations import * 
from collections import defaultdict
from collections import OrderedDict
import cPickle as p
import csv
from helper import *
import os.path
import pdb
import sys
from tf_idf import *
import time
from topic_modeling import *
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")

def generate_interesting_phrases_per_topic(headlines, stories, take_texts, topics):
    topic_dict = defaultdict(int)
    for idx in topics:
        topics[idx] = list(set(topics[idx]))
        for t in topics[idx]:
            topic_dict[t] += 1
    topic_dict = OrderedDict(sorted(topic_dict.items(), key=lambda x: x[1], reverse=True))
    freq_topics = topic_dict.keys()[2:102] # Top two topics (LEN & RETR) appear in all docs
    for topic in freq_topics:
        print topic
        generate_interesting_bigram_phrases(headlines, stories, take_texts, topics, topic)
        generate_interesting_trigram_phrases(headlines, stories, take_texts, topics, topic)        
        
def main(args):
    if os.path.exists("headlines.p"):
        start_time = time.time()
        print 'Reading cached data...'
        headlines = p.load(open("headlines.p", 'rb'))
        stories = p.load(open("stories.p", 'rb'))
        take_texts = p.load(open("take_texts.p", 'rb'))
        topics = p.load(open("topics.p", 'rb'))
        print 'Done! Time taken: ', time.time() - start_time
    else:
        headlines = defaultdict(str)
        stories = defaultdict(str)
        take_texts = defaultdict(str)
        topics = defaultdict(list)
        ct = 0
        start_time = time.time()
        print 'Reading data...'
        with open(args.data_csv_filename) as csvfile:
            data_reader = csv.DictReader(csvfile, delimiter=',')
            for row in data_reader:
                lang = row['LANGUAGE']
                if lang != 'EN': #Ignoring non-english text
                    continue
                if row['PRODUCTS'] == 'TEST': #Ignoring test messages
                    continue
                idx = row['UNIQUE_STORY_INDEX']
                
                topics[idx] += row['TOPICS'].split()
                
                if row['EVENT_TYPE'] == 'ALERT':
                    headlines[idx] = row['HEADLINE_ALERT_TEXT']
                    stories[idx] = row['ACCUMULATED_STORY_TEXT']
                    take_texts[idx] = row['TAKE_TEXT']
                elif row['EVENT_TYPE'] == 'HEADLINE':
                    headlines[idx] = row['HEADLINE_ALERT_TEXT']
                    stories[idx] = row['ACCUMULATED_STORY_TEXT']
                    # row['TAKE_TEXT'] is always empty here
                elif row['EVENT_TYPE'] == 'STORY_TAKE_OVERWRITE':
                    # row['HEADLINE_ALERT_TEXT'] can be empty when original headlines[idx] is not
                    # row['ACCUMULATED_STORY_TEXT'] is always empty here
                    take_texts[idx] = row['TAKE_TEXT']
                elif row['EVENT_TYPE'] == 'STORY_TAKE_APPEND':
                    stories[idx] = row['ACCUMULATED_STORY_TEXT']
                    take_texts[idx] = row['TAKE_TEXT']
    
                ct += 1
                if ct > 1000:
                    break
        
        print 'Done! Time taken: ', time.time() - start_time
        
        start_time = time.time()
        print 'Running processing...'
        headlines, stories, take_texts = preprocess_data(headlines, stories, take_texts)            
        print 'Done! Time taken: ', time.time() - start_time
    
        p.dump(headlines, open("headlines.p", 'wb'))
        p.dump(stories, open("stories.p", 'wb'))
        p.dump(take_texts, open("take_texts.p", 'wb'))
        p.dump(topics, open("topics.p", 'wb'))
        
    return

    if args.headlines_only:
        print 'Using only headlines!'
        news_contents = headlines
    else:
        news_contents = combine_texts(headlines, stories, take_texts)
    
    if args.tf_idf:
        print 'Finding interesting words using TF-IDF'
        tf_idf(news_contents, MAX_COUNT=100)
    
    if args.collocations:
        print 'Finding interesting bigram phrases using collocations'
        bigram_collocations(news_contents, MAX_COUNT=100)
        print 'Finding interesting trigram phrases using collocations'
        trigram_collocations(news_contents, MAX_COUNT=100)
        
    if args.topic_modeling:
        print 'Finding interesting words using topic modeling'
        generate_interesting_words(news_contents)
        print 'Finding interesting bigram phrases using topic modeling'
        generate_interesting_bigram_phrases(news_contents)
        print 'Finding interesting trigram phrases using topic modeling'
        generate_interesting_trigram_phrases(news_contents)

        #generate_interesting_phrases_per_topic(news_contents, topics)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--data_csv_filename", type = str)
    argparser.add_argument("--headlines_only", type = bool)
    argparser.add_argument("--tf_idf", type = bool)
    argparser.add_argument("--collocations", type = bool)
    argparser.add_argument("--topic_modeling", type = bool)
    args = argparser.parse_args()
    print args
    print ""
    main(args)