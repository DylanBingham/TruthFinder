from flask import Flask, request, jsonify, send_from_directory
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

from utils import (
    extract_features_from_article, setup_input_articles
)

import datetime
import json
import os

setup_input_articles()

app = Flask(__name__)
CORS(app)

# Sample dictionary of articles. You can map either titles or URLs to article text.
articles = {
    "sample_article": "This is the sample article text to be processed by the feature extraction functions.",
    "https://example.com/article1": "Another article text with some different content."
}

# Define a route to extract features for an article specified by title or URL
@app.route('/extract_features', methods=['POST'])
def extract_features_route():
    logging.debug("Received request to extract features.")
    data = request.get_json()
    logging.debug(f"Request data: {data}")
    article_title = data.get("article_title")
    url = data.get("url")
    
    print(f"Article title: {article_title}")
    print(f"URL: {url}")
    print(f"rticle_text: {article_text}")

    # Lookup the article text using the provided article_title or url
    if article_title and article_title in articles:
        article_text = articles[article_title]
    elif url and url in articles:
        article_text = articles[url]
    else:
        logging.warning("Article not found.")
        return jsonify({"error": "Article not found."}), 404

    # Extract features from the article text
    features = extract_features_from_article(article_text)
    logging.debug(f"Extracted features: {features}")
    return jsonify(features)


# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


global_resp_data = {}

# Your existing API routes
@app.route('/save_url', methods=['POST'])
def save_url():
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
    # print(f'Input text (first 30 characters) is {input_text[0:30]}')
    f,pred = extract_features_from_article(input_text)
    logging.debug("----------------------------------------------------------------------------------------")
    logging.debug(f"Extracted features: {f}")
    logging.debug(f"Prediction: {pred}")
    logging.info("EXTRACTED FEATURES:----------------------------------------------------------------------------------------")
    
    
    # print(f'Model Result: {pred}')
    
    current_time = datetime.datetime.now()



  


    def calculate_confidence(pred):
        # Map the overall score to a confidence descriptor.
        if pred < 0.2:
            descriptor = "It is very unlikely to be true."
        elif pred < 0.4:
            descriptor = "It is unlikely to be true."
        elif pred < 0.6:
            descriptor = "It is somewhat likely to be true."
        elif pred < 0.8:
            descriptor = "It is likely to be true."
        else:
            descriptor = "It is very likely to be true."
        
        return descriptor
    

    confidence_string = calculate_confidence( pred )

    logging.info(f"Confidence String: {confidence_string}")

    global_resp_data = [
        {
            "fake_percent": round(pred*100,2),  
            "fake_percent_display": confidence_string, 
            "confidence": 0,
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

    try:
        with open("output_data.json", 'w') as file:
            json.dump(global_resp_data, file, indent=4)
            logging.info("Data successfully written to output_data.json.")
    except Exception as e:
        logging.error(f"An error occurred while writing to output_data.json: {e}")
    
    logging.debug("----------------------------------------------------------------------------------------")


    if not url:
        return jsonify({"error": "No URL provided"}), 400

    with open("input_url.txt", "w") as file:
        file.write(url)


    return jsonify({"message": "URL saved successfully"})

@app.route('/get_output', methods=['GET'])

def get_output():
    logging.debug("Received request to get output data.")
    try:
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_data.json')
        logging.debug(f"Looking for file at: {filepath}")
        
        # Check if file exists
        if not os.path.exists(filepath):
            logging.warning(f"{datetime.now()} - output_data.json not found at {filepath}")
            return jsonify({"error": "Data file not found"}), 404
        
        # Check file permissions
        if not os.access(filepath, os.R_OK):
            logging.warning(f"{datetime.now()} - Permission denied for {filepath}")
            return jsonify({"error": "Cannot read data file"}), 403
        
        # Read and validate file
        with open(filepath, 'r') as file:
            data = json.load(file)
            
            # Validate data structure
            if not isinstance(data, list) or len(data) == 0:
                logging.error(f"{datetime.now()} - Invalid data format in file")
                return jsonify({"error": "Invalid data format"}), 500
                
            if 'fake_percent' not in data[0]:
                logging.error(f"{datetime.now()} - Missing required fields")
                return jsonify({"error": "Missing data fields"}), 500
                
        logging.info("Successfully retrieved output data.")
        return jsonify(data)
        
    except json.JSONDecodeError:
        logging.error(f"{datetime.now()} - Invalid JSON in file")
        return jsonify({"error": "Corrupted data file"}), 500
    except Exception as e:
        logging.error(f"{datetime.now()} - Unexpected error: {str(e)}")
        return jsonify({"error": "Server error"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)