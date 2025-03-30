# Topic Identification
# https://www.analyticsvidhya.com/blog/2022/02/topic-identification-with-gensim-library-using-python/
# https://www.youtube.com/watch?v=OYze4BQtn-U
#https://medium.com/blend360/topic-modelling-a-comparison-between-lda-nmf-bertopic-and-top2vec-part-i-3c16372d51f0
# last one has good refs for lit review!

# https://www.youtube.com/watch?v=_QiTQQDrx5I

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
nltk.download("stopwords")
from nltk.corpus import stopwords

stopword_list = stopwords.words('english')

stopword_list.extend(["reuters", "monday", "tuesday", "wednesday", "thursday", "friday", "2016", "2017", "2018", "2019", "2020"])

#https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(
    stop_words = stopword_list, min_df = 20, max_df = 0.95, ngram_range = (1,2), strip_accents = 'unicode', max_features = 1000) 


tfidf = tfidf_vectorizer.fit_transform(text_list)

tfidf_vectorizer.get_feature_names_out()

num_topics = 20
model = decomposition.NMF(n_components=num_topics, random_state = 42) 
W = model.fit_transform(tfidf)
H = model.components_

# extract significant words in each topic

num_words = 15

# get feature names as array
vocab = np.array(tfidf_vectorizer.get_feature_names_out())
# higher coefficients towards end of array, pick last 15 words
top_words = lambda t: [vocab[i] for i in np.argsort(t)[:-num_words-1:-1]]
# get top words from H matrix
topic_words = ([top_words(t) for t in H])
topics = [" ".join(t) for t in topic_words]


# build topic and word dataframe

topics

news_data["subject"].unique()

subject_list = news_data["subject"].tolist()

tfidf2 = tfidf_vectorizer.fit_transform(subject_list)

tfidf_vectorizer.get_feature_names_out()

num_topics = 20
model = decomposition.NMF(n_components=num_topics, random_state = 42) 
W = model.fit_transform(tfidf2)
H = model.components_

num_words = 15

# get feature names as array
vocab = np.array(tfidf_vectorizer.get_feature_names_out())
# higher coefficients towards end of array, pick last 15 words
top_words = lambda t: [vocab[i] for i in np.argsort(t)[:-num_words-1:-1]]
# get top words from H matrix
topic_words = ([top_words(t) for t in H])
topics = [" ".join(t) for t in topic_words]

topics

## We could simplify this and make it a factor, is it political news or not? But generated topics were not useful by themselves 
# (different mixtures of political buzz words, since dataset unbalanced by topic (some datasets from 2017 were following the heels of the 2016 US election)



