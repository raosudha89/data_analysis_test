# Prerequisites

1. Install gensim, nltk, sklearn, pyLDAvis.gensim, unidecode
   pip install gensim, nltk, sklearn, pyLDAvis.gensim, unidecode

2. Install wordcloud (https://github.com/amueller/word_cloud)
   pip install wordcloud

----------------------------------------------------------------------------------------------------

# Structure

** All scripts are included in the src directory
** All outputs are included in the output directory
** All visualizations are included in the visualizations directory
** All references are included in the scripts

----------------------------------------------------------------------------------------------------

# Main Ideas

** We extract text containing in these three fields of the data: 
   'HEADLINE_ALERT_TEXT', 'ACCUMULATED_STORY_TEXT', 'TAKE_TEXT'

** We ignore non-english data since approx 80% of the data is in english.
   We also ingore TEST messages (PRODUCT=='TEST')

** We process data using following steps:
   a. Remove non-ascii characters
   b. Lower case
   c. Remove punctuations
   d. Remove numbers
   c. Tokenize
   d. Stopword removal

** We implement two key ideas for identifying interesting words/phrases
   1. Term Frequency - Inverse Document Frequency (TF-IDF)
      This simple method helps us identify salient words that occur frequently 
      in a few documents (but not in most documents).

   2. Topic Modeling using Latent Direchlet Allocation (LDA)
      This method helps us identify latent topics in the dataset.
      Additionally, it also provides a distribution of words that belong to those topics.
      We use this method, to identify salient topic words in the data.

      To identify interesting phrases, we extract bigrams and trigrams out of the text.
      And then use topic modeling to identify salient phrases in the data. 

----------------------------------------------------------------------------------------------------

# Generating interesting words using TF-IDF

** python src/main.py	--data_csv_filename data/rna002_RTRS_2013_06.csv \
			--tf_idf True \
			--tf_idf_max_count 100 \

** Above script generates top 100 words with the highest tf-idf value (summed across all documents).
   You can change the value of the argument "tf_idf_max_count" to generate more words.

** Output:
   Top 100 words generated using the entire dataset is included in output/tf_idf/tf_idf_100.txt

** Visualization: 
   Above script also generates a word cloud of the words which is saved as an image named "tf_idf_100" in the current directory  
   Word cloud of top 100 words generated using the entire dataset is included in visualizations/tf_idf/tf_idf_100.png

----------------------------------------------------------------------------------------------------

# Generating interesting words using TF-IDF per TOPIC

** The input csv data file contains "TOPICS" metadata which contains the different topics the news article belongs to. 
   We make use of this metatdata to identify interesting words per TOPIC

** python src/main.py   --data_csv_filename data/rna002_RTRS_2013_06.csv \
			--tf_idf_max_count 100 \
			--tf_idf_per_topic True \
			--freq_topics_count 10 \

** Above script generates interesting words per TOPIC (E.g. US, ASIA, CMPNY, EMRG, etc) for 10 most frequent TOPICS.
   You can change the value of the argument "freq_topics_count" to generate words for more TOPICS. 

** Output:
   Top 100 words per TOPIC for 10 most frequent TOPICS is included in output/tf_idf/tf_idf_TOPIC_NAME_100.txt
   
** Visualization: 
   Word cloud of top 100 words per TOPIC for 10 most frequent TOPICS is included in 
   visualizations/tf_idf/tf_idf_TOPIC_NAME_100.png

----------------------------------------------------------------------------------------------------

# Generating interesting words & phrases using Topic Modeling (LDA)

** python src/main.py   --data_csv_filename data/rna002_RTRS_2013_06.csv \
			--topic_modeling True \
			--topic_modeling_num_topics 10 \

** Above script identifies 10 different topics and generates interesting 30 words per each topic.
   (Note that these topics are latent and are different from the TOPICS included in the metadata.)
   In addition, it also generates 30 bigram & trigram phrases per each topic. 
   (Note that the topics are generated idependently for the unigrams, bigrams & trigrams.) 
   You can change the value of the argument "topic_modeling_num_topics" to generate more number of topics.


** Output:
   Top 30 words, bigrams & trigrams for 10 topics are included in the location:
   Unigrams: output/topic_modeling/topic_modeling_words.txt
   Bigrams:  output/topic_modeling/topic_modeling_bigrams.txt
   Trigrams: output/topic_modeling/topic_modeling_trigrams.txt

** Visualization:
   Above script also generates a nice visualization for the topic modeling output. 
   Visualization for the 30 unigrams, bigrams & trigrams for 10 topics are included in the location:
   Unigrams: visualizations/topic_modeling/topic_modeling_words.html 
   Bigrams:  visualizations/topic_modeling/topic_modeling_bigrams.html
   Trigrams: visualizations/topic_modeling/topic_modeling_trigrams.html

   In the above visualization, the 10 circles to the left denote the 10 topics and how they are related to each other.
   The words and bar graphs to the right denote the top 30 words corresponding to the 10 topics.
   If you hover over a topic on the left (i.e. hover on a circle), then the bar graphs to the right will 
   show the frequency of the words belonging to that topic. 
   If you hover over a particular word on the right, then the circles to the left will enlarge in propotionally
   to the frequency of the word in a topic.  

----------------------------------------------------------------------------------------------------

# Generating interesting words & phrases using Topic Modeling (LDA) per topic

** The input csv data file contains "TOPICS" metadata which contains the different topics the news article belongs to. 
   Same as in TF-IDF, we make use of this metatdata to identify interesting words per topic

** python src/main.py   --data_csv_filename data/rna002_RTRS_2013_06.csv \
			--topic_modeling_per_topic True \
			--topic_modeling_num_topics 10 \
			--freq_topics_count 5 \

** For each TOPIC, the above script identifies 10 subtopics and generates 30 interesting words, bigrams & trigrams per subtopic.
   You can change the value of the argument "freq_topics_count" to generate words for more TOPICS.
   You can change the value of the argument "topic_modeling_num_topics" to generate more number of subtopics.

** Output:
   For 5 most frequent TOPICS, top 30 words, bigrams & trigrams for 10 subtopics are included in the location:
   Unigrams: output/topic_modeling/topic_modeling_words_TOPIC_NAME.txt
   Bigrams:  output/topic_modeling/topic_modeling_bigrams_TOPIC_NAME.txt
   Trigrams: output/topic_modeling/topic_modeling_trigrams_TOPIC_NAME.txt

** Visualization:
   Visualization for the 30 unigrams, bigrams & trigrams are included in the location:
   Unigrams: visualizations/topic_modeling/topic_modeling_words_TOPIC_NAME.html 
   Bigrams:  visualizations/topic_modeling/topic_modeling_bigrams_TOPIC_NAME.html
   Trigrams: visualizations/topic_modeling/topic_modeling_trigrams_TOPIC_NAME.html

----------------------------------------------------------------------------------------------------

# Using only headlines

** All of the configurations above can be run with an additional --only_headlines argument.
   This will cause the script to use only the 'HEADLINE_ALERT_TEXT' field of data to find interesting words & phrases. 

