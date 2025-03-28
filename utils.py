from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np
import pandas as pd
import nltk
import re
import textstat

nltk.download('punkt_tab')

# Define a function to clean text
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Use NLTK tokenizer
    tokens = word_tokenize(text)
    return (text, tokens)


# Function to extract features from a single article text
def extract_features(article_text):
    # Clean the text
    cleaned_text, tokens = clean_text(article_text)
    
    # Create the TF-IDF vectorizer and compute TF-IDF features on a single document
    tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform([cleaned_text])
    
    # Get the TF-IDF feature values (since it's a single document, take the first row)
    tfidf_values = tfidf_matrix.toarray()[0]
    
    # Compute the Flesch reading ease score for the cleaned text
    reading_ease_score = textstat.flesch_reading_ease(cleaned_text)
    
    # Create a features dictionary: include each TF-IDF feature (keyed by term) and the reading ease score
    features = {f"tfidf_{term}": tfidf_values[i] 
                for i, term in enumerate(tfidf_vectorizer.get_feature_names_out())}
    features["flesch_reading_ease"] = reading_ease_score
    
    return features

# Example usage:
# article = "This is an example article. It includes numbers like 123, punctuation, and multiple sentences."
# features = extract_features(article)
# print(features)