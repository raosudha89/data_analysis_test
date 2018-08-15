import nltk
from nltk.corpus import stopwords
import re
import string
from unidecode import unidecode

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def preprocess(text, remove_numbers=False):
    if text == '':
        return text
    text = remove_non_ascii(text)
    text = text.lower()
    text = text.translate(None, string.punctuation)
    if remove_numbers:
        text = re.sub(r'[0-9]+', '', text)
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if not w in stopwords.words('english')]
    return ' '.join(tokens)