import nltk
from nltk.corpus import stopwords
import pdb
import re
import string
from unidecode import unidecode
cachedStopWords = stopwords.words("english")

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def preprocess_data(headlines, stories, take_texts):
    for idx in headlines:
        headlines[idx] = preprocess(headlines[idx], remove_numbers=True)
        stories[idx] = preprocess(stories[idx], remove_numbers=True)
        take_texts[idx] = preprocess(take_texts[idx], remove_numbers=True)
    return headlines, stories, take_texts

def preprocess(text, remove_numbers=False):
    if text == '':
        return text
    text = remove_non_ascii(text)
    text = text.lower()
    text = text.translate(None, string.punctuation)
    if remove_numbers:
        text = re.sub(r'[0-9]+', '', text)
    tokens = nltk.word_tokenize(text)
    pattern = re.compile(r'\b(' + r'|'.join(cachedStopWords) + r')\b\s*')
    text = pattern.sub('', text)
    return text

def combine_texts(headlines, stories, take_texts):
    contents = {}
    for idx in headlines:
        contents[idx] = headlines[idx] + stories[idx] + take_texts[idx]
    return contents

def get_freq_topics(topics, TOPIC_COUNT=100):
    topic_dict = defaultdict(int)
    for idx in topics:
        topics[idx] = list(set(topics[idx]))
        for t in topics[idx]:
            topic_dict[t] += 1
    topic_dict = OrderedDict(sorted(topic_dict.items(), key=lambda x: x[1], reverse=True))
    freq_topics = topic_dict.keys()[2:2+TOPIC_COUNT] # Top two topics (LEN & RETR) appear in all docs, hence ignore
    return freq_topics
