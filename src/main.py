import argparse
from collections import defaultdict
import cPickle as p
import csv
from helper import *
import os.path
import pdb
import sys
from tf_idf import *
import time
from topic_modeling import *

def update_data(row, headlines, stories, take_texts, topics):
    idx = row['UNIQUE_STORY_INDEX']
    topics[idx] += row['TOPICS'].split()
    if row['EVENT_TYPE'] == 'ALERT':
        headlines[idx] = row['HEADLINE_ALERT_TEXT']
        stories[idx] = row['ACCUMULATED_STORY_TEXT']
        take_texts[idx] = row['TAKE_TEXT']
    elif row['EVENT_TYPE'] == 'HEADLINE': # Ignore TAKE_TEXT since always empty 
        headlines[idx] = row['HEADLINE_ALERT_TEXT']
        stories[idx] = row['ACCUMULATED_STORY_TEXT']
    elif row['EVENT_TYPE'] == 'STORY_TAKE_OVERWRITE': # Only overwrite TAKE_TEXT
        take_texts[idx] = row['TAKE_TEXT']
    elif row['EVENT_TYPE'] == 'STORY_TAKE_APPEND':
        stories[idx] = row['ACCUMULATED_STORY_TEXT']
        take_texts[idx] = row['TAKE_TEXT']
    return headlines, stories, take_texts, topics
        
def main(args):
    if os.path.exists("headlines.p"): # Load from cached data if present
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
                headlines, stories, take_texts, topics = update_data(row, headlines, stories, take_texts, topics)
        print 'Done! Time taken: ', time.time() - start_time
        
        start_time = time.time()
        print 'Running processing...'
        headlines, stories, take_texts = preprocess_data(headlines, stories, take_texts)            
        print 'Done! Time taken: ', time.time() - start_time
    
        # Cache data as picked files    
        p.dump(headlines, open("headlines.p", 'wb'))
        p.dump(stories, open("stories.p", 'wb'))
        p.dump(take_texts, open("take_texts.p", 'wb'))
        p.dump(topics, open("topics.p", 'wb'))

    # Use the "TOPICS" metadata in csv file to identify frequently occurring topics across documents
    freq_topics = get_freq_topics(topics, TOPIC_COUNT=args.freq_topics_count)

    if args.headlines_only:
        print 'Using only headlines!'
        news_contents = headlines
    else:
        # Combine text contained in 'HEADLINE_ALERT_TEXT', 'ACCUMULATED_STORY_TEXT', 'TAKE_TEXT'
        # to form a document
        news_contents = combine_texts(headlines, stories, take_texts)
    
    if args.tf_idf:
        print 'Finding interesting words using TF-IDF'
        start_time = time.time()
        tf_idf(news_contents, args.tf_idf_max_count)
        print 'Done! Time taken ', time.time() - start_time
    
    if args.tf_idf_per_topic:
        print 'Finding interesting words per topic using TF-IDF'
        start_time = time.time()
        tf_idf_per_topic(news_contents, args.tf_idf_max_count, topics, freq_topics)
        print 'Done! Time taken ', time.time() - start_time
        
    if args.topic_modeling:
        topic_modeling(news_contents, args.topic_modeling_num_topics)
    
    if args.topic_modeling_per_topic:
        topic_modeling_per_topic(news_contents, topics, freq_topics, args.topic_modeling_num_topics)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--data_csv_filename", type = str)
    argparser.add_argument("--headlines_only", type = bool)
    argparser.add_argument("--freq_topics_count", type = int, default=10)
    argparser.add_argument("--tf_idf", type = bool)
    argparser.add_argument("--tf_idf_max_count", type = int, default=100)
    argparser.add_argument("--tf_idf_per_topic", type = bool)
    argparser.add_argument("--topic_modeling", type = bool)
    argparser.add_argument("--topic_modeling_num_topics", type = int, default=10)
    argparser.add_argument("--topic_modeling_per_topic", type = bool)
    args = argparser.parse_args()
    print args
    print ""
    main(args)