import matplotlib.pyplot as plt
import pyLDAvis.gensim
from wordcloud import WordCloud

# Reference: https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21
def visualize_topics(ldamodel, corpus, dictionary, out_fname):
    lda_display = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(lda_display, out_fname+'.html')
    
# Reference: https://github.com/amueller/word_cloud    
def word_cloud(text, fname):
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(fname, dpi=1200)

