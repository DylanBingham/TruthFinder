import pandas as pd
import numpy as np
import seaborn as sb

from utils import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer


# Load the dataset
dataset = pd.read_csv('data/processed_combined_data.csv', usecols=[0,1,2,3,4,5,6,7,8,9], index_col=0)

dataset.head()


#########
# CREATE - TFIDF vectors
#########

# Drop rows where 'text' is missing
dataset = dataset[dataset['text'].notnull()].copy()

# Optional: Preprocess text (e.g., lowercasing)
dataset['text_clean'] = dataset['text'].apply(clean_text)

# Initialize the TF-Idataset Vectorizer with a maximum number of features and English stopwords removal
tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')

# Fit and transform the cleaned text into a TF-Idataset feature matrix
tfidf_matrix = tfidf_vectorizer.fit_transform(dataset['text_clean'])

# Convert the TF-Idataset matrix to a DataFrame for inspection or further processing
tfidf_dataset = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

# Optionally, add the label column for reference in further analysis
tfidf_dataset['label'] = dataset['label'].values

# Display the first few rows of the TF-Idataset features
print(tfidf_dataset.head())
