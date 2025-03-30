from textblob import TextBlob
import nltk
import numpy as np

# removing strange characters
def clean_encoding(text):
    text = text = text.replace('â€˜', "'").replace('â€™', "'").replace('â€œ', '"').replace('â€', '"')
    text = text.replace('â€“', '–').replace('â€”', '—').replace('â€', '')
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return text

# Get article word count
def get_article_word_count(article):
    return len(article.split())

# Get overall sentiment scores
def find_polarity(news_story):
    news = TextBlob(news_story)
    return news.sentiment.polarity

def find_subjectivity(news_story):
    news = TextBlob(news_story)
    return news.sentiment.subjectivity

# Get sentence average sentiment scores
# ChatGPT sped up these functions by replacing looping and appending to a list with a list comprehension

def find_avg_polarity_sentences(news_story):
    # Create the TextBlob object once
    news = TextBlob(news_story)
    # Use list comprehension to extract polarity in one go
    polarities = [sentence.sentiment.polarity for sentence in news.sentences]
    return sum(polarities) / len(polarities) if polarities else 0  # Avoid division by zero

def find_avg_subjectivity_sentences(news_story):
    # Create the TextBlob object once
    news = TextBlob(news_story)
    # Use list comprehension to extract subjectivity in one go
    subjectivities = [sentence.sentiment.subjectivity for sentence in news.sentences]
    return sum(subjectivities) / len(subjectivities) if subjectivities else 0  # Avoid division by zero

# Get number of speech tags
def get_num_speech_attributes(text):
    text = text.lower()
    return text.count("said") + text.count("say") + text.count("told") + text.count("tell")


# Compile feature extraction function
def create_article_info(article_text):
    article_info = {}
    article_text = clean_encoding(article_text) # Clean the text first
    # Extract features
    article_info['word_count'] = get_article_word_count(article_text)
    article_info['polarity'] = find_polarity(article_text)
    article_info['subjectivity'] = find_subjectivity(article_text)
    article_info['avg_polarity'] = find_avg_polarity_sentences(article_text)
    article_info['avg_subjectivity'] = find_avg_subjectivity_sentences(article_text)
    article_info['num_speech_tags'] = get_num_speech_attributes(article_text)
    return article_info
