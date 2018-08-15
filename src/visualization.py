import matplotlib.pyplot as plt
import pyLDAvis.gensim
from wordcloud import WordCloud

def visualize_topics(ldamodel, corpus, dictionary):
    lda_display = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary, sort_topics=False)
    pyLDAvis.show(lda_display)
    
def word_cloud(text):
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

