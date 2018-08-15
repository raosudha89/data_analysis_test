import argparse
#from collocations import * 
from collections import defaultdict
from collections import OrderedDict
import csv
from helper import *
import pdb
import sys
#from tf_idf import *
from topic_modeling import *

def generate_interesting_phrases_per_topic(headlines, stories, take_texts, topics):
    topic_dict = defaultdict(int)
    for idx in topics:
        topics[idx] = list(set(topics[idx]))
        for t in topics[idx]:
            topic_dict[t] += 1
    topic_dict = OrderedDict(sorted(topic_dict.items(), key=lambda x: x[1], reverse=True))
    i = 0
    freq_topics_count = 100
    for topic, ct in topic_dict.iteritems():
        if ct == len(headlines):
            continue
        print topic
        i += 1
        if i > freq_topics_count:
            break
        generate_interesting_bigram_phrases(headlines, stories, take_texts, topics, topic)
        generate_interesting_trigram_phrases(headlines, stories, take_texts, topics, topic)
    
def main(args):
    headlines = defaultdict(str)
    stories = defaultdict(str)
    take_texts = defaultdict(str)
    topics = defaultdict(list)
    ct = 0
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
                headlines[idx] = preprocess(row['HEADLINE_ALERT_TEXT'])
                #stories[idx] = preprocess(row['ACCUMULATED_STORY_TEXT'], remove_numbers=True)
                #take_texts[idx] = preprocess(row['TAKE_TEXT'], remove_numbers=True)
            elif row['EVENT_TYPE'] == 'HEADLINE':
                headlines[idx] = preprocess(row['HEADLINE_ALERT_TEXT'])
                #stories[idx] = preprocess(row['ACCUMULATED_STORY_TEXT'], remove_numbers=True)
                # row['TAKE_TEXT'] is always empty here
            #elif row['EVENT_TYPE'] == 'STORY_TAKE_OVERWRITE':
                # row['HEADLINE_ALERT_TEXT'] can be empty when original headlines[idx] is not
                # row['ACCUMULATED_STORY_TEXT'] is always empty here
            #    take_texts[idx] = preprocess(row['TAKE_TEXT'], remove_numbers=True)
            #elif row['EVENT_TYPE'] == 'STORY_TAKE_APPEND':
            #    stories[idx] = preprocess(row['ACCUMULATED_STORY_TEXT'], remove_numbers=True)
            #    take_texts[idx] = preprocess(row['TAKE_TEXT'], remove_numbers=True)

            ct += 1
            if ct > 10000:
                break
    
    #word_cloud(' . '.join(headlines.values()))
    
    #generate_interesting_words(headlines, stories, take_texts)
    generate_interesting_bigram_phrases(headlines, stories, take_texts)
    #generate_interesting_trigram_phrases(headlines, stories, take_texts)

    #generate_interesting_phrases_per_topic(headlines, stories, take_texts, topics)
    
    #collocations(headlines)
    #collocations(contents)
            
    #tf_idf(headlines)
    #tf_idf(stories)
    #tf_idf(take_texts)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--data_csv_filename", type = str)
    args = argparser.parse_args()
    print args
    print ""
    main(args)