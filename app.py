from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
import os
import json
import pickle
from utils import extract_features_from_article
import datetime
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# Module-level variable to store the response data
shared_response_data = None

# Sample dictionary of articles. You can map either titles or URLs to article text.
articles = {
    "sample_article": "This is the sample article text to be processed by the feature extraction functions.",
    "https://example.com/article1": "Another article text with some different content."
}

# Define a route to extract features for an article specified by title or URL
# @app.route('/extract_features', methods=['POST'])
# def extract_features_route():
#     logging.debug("Received request to extract features.")
#     data = request.get_json()
#     logging.debug(f"Request data: {data}")
#     article_title = data.get("article_title")
#     url = data.get("url")
    
#     # Lookup the article text using the provided article_title or url
#     if article_title and article_title in articles:
#         article_text = articles[article_title]
#     elif url and url in articles:
#         article_text = articles[url]
#     else:
#         logging.warning("Article not found.")
#         return jsonify({"error": "Article not found."}), 404

#     # Extract features from the article text
#     features = extract_features_from_article(article_text)
#     logging.debug(f"Extracted features: {features}")
#     return jsonify(features)


# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    if filename.endswith('.csv'):
        return send_from_directory('static', filename, mimetype='text/csv')
    return send_from_directory('static', filename)


global_resp_data = {}

# Your existing API routes
@app.route('/save_url', methods=['POST'])
def save_url():
    global shared_response_data  # Access the module-level variable
    
    logging.debug("Received request to save URL.")
    try:
        data = request.get_json()
        logging.debug(f"Request data: {data}")
    except Exception as e:
        logging.error(f"Error parsing JSON: {e}")
        return jsonify({"error": "Invalid JSON"}), 400

    url = data.get("url") if data else None

    if not url:
        logging.warning("No URL provided in request.")
        return jsonify({"error": "No URL provided"}), 400

    logging.info(f"Processing URL: {url}")
    
    def extract_text(url):
        with open("article_text.pkl", "rb") as file:
            d = pickle.load(file)
        return d[url]
    
    input_text = extract_text(url)
    f, pred = extract_features_from_article(input_text)
    logging.debug("----------------------------------------------------------------------------------------")
    logging.debug(f"Extracted features: {f}")
    logging.debug(f"Prediction: {pred}")
    logging.info("EXTRACTED FEATURES:----------------------------------------------------------------------------------------")
    
    
    # print(f'Model Result: {pred}')
    
    current_time = datetime.now()



  


    def calculate_confidence(polarity, subjectivity, word_count, quotes, flesch_reading_ease, pred: int):
        """
        Calculate an overall confidence score based on five parameters:
        
        - polarity: [-1, 1], where 0 is most balanced.
        - subjectivity: [0, 1], where 0 is factual.
        - word_count: total number of words (benchmark: 1000 words for maximum contribution).
        - quotes: count of quotation signals (benchmark: 20 quotes for maximum contribution).
        - flesch_reading_ease: [1, 100], where 100 is easiest to read.
        
        Returns:
        overall_confidence (float): Combined confidence score between 0 and 1.
        descriptor (str): A brief descriptive string.
        """
        # Normalize each parameter:
        polarity_factor = 1 - abs(polarity)             # Best if sentiment is neutral.
        subjectivity_factor = 1 - subjectivity           # Best if content is factual.
        
        # We assume that 1000 words is our benchmark for a full score.
        normalized_word_count = min(1.0, word_count / 1000.0)
        
        # We assume that 20 quotes would be excellent; adjust as needed.
        normalized_quotes = min(1.0, quotes / 20.0)
        
        # Normalize Flesch Reading Ease so that a score of 1 maps to 0 and 100 maps to 1.
        normalized_readability = (flesch_reading_ease - 1) / 99.0
        
        # Compute the overall confidence as an equally weighted average.
        overall_confidence = (polarity_factor +
                            subjectivity_factor +
                            normalized_word_count +
                            normalized_quotes +
                            normalized_readability) / 5
        
        overall_confidence = round(pred, 2)  # Round to two decimal places for clarity.
        # Map the overall score to a confidence descriptor.
        if overall_confidence < 0.25:
            descriptor = "very low credibility"
        elif overall_confidence < 0.4:
            descriptor = "low credibility"
        elif overall_confidence < 0.7:
            descriptor = "moderate credibility"
        elif overall_confidence < 0.85:
            descriptor = "high credibility"
        else:
            descriptor = "very high credibility"
        

        return overall_confidence, descriptor
    

    confidence_score, confidence_string = calculate_confidence( round(f['overall_polarity'], 2), round(f['overall_subjectivity'], 2), round(f['word_count'], 0), round(f['num_speech_attributes'], 0), round(f['flesch_reading_ease'], 0), pred)

    logging.info(f"Confidence Score: {confidence_score}")
    logging.info(f"Confidence String: {confidence_string}")

    current_time = datetime.now()
    
    shared_response_data = [
        {
            "fake_percent": pred*100,  
            "fake_percent_display": confidence_string, 
            "confidence": confidence_score,
            "last_updated": current_time.isoformat(),
            "polarity_score": round(f['overall_polarity'],2),
            "subjectivity_score": round(f['overall_subjectivity'],2),
            "avg_polarity": round(f['avg_sentence_polarity'],2),
            "avg_subjectivity": round(f['avg_sentence_subjectivity'],2),  
            "num_quotes": round(f['num_speech_attributes'],0),
            "word_count": round(f['word_count'],0),
            "flesch_reading_ease": round(f['flesch_reading_ease'],0)
        }
    ]

    return jsonify({"message": "URL saved successfully"})

@app.route('/get_output', methods=['GET'])
def get_output():
    global shared_response_data  # Access the module-level variable
    
    logging.debug("Received request to get output data.")
    
    if shared_response_data is None:
        logging.warning("No data available yet")
        return jsonify({"error": "No data available yet"}), 404
        
    try:
        # Validate data structure
        if not isinstance(shared_response_data, list) or len(shared_response_data) == 0:
            logging.error("Invalid data format in shared data")
            return jsonify({"error": "Invalid data format"}), 500
            
        if 'fake_percent' not in shared_response_data[0]:
            logging.error("Missing required fields")
            return jsonify({"error": "Missing data fields"}), 500
            
        logging.info("Successfully retrieved output data.")
        return jsonify(shared_response_data)
        
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)