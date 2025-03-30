from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import (
    extract_features
)

import datetime
import json
import os


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
    data = request.get_json()
    article_title = data.get("article_title")
    url = data.get("url")
    
    # Lookup the article text using the provided article_title or url
    if article_title and article_title in articles:
        article_text = articles[article_title]
    elif url and url in articles:
        article_text = articles[url]
    else:
        return jsonify({"error": "Article not found."}), 404

    # Extract features from the article text
    features = extract_features(article_text)
    return jsonify(features)

# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Your existing API routes
@app.route('/save_url', methods=['POST'])
def save_url():
    try:
        data = request.get_json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": "Invalid JSON"}), 400

    url = data.get("url") if data else None
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    with open("input_url.txt", "w") as file:
        file.write(url)

    return jsonify({"message": "URL saved successfully"})

@app.route('/get_output', methods=['GET'])
def get_output():
    try:
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_data.json')
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"{datetime.now()} - output_data.json not found at {filepath}")
            return jsonify({"error": "Data file not found"}), 404
        
        # Check file permissions
        if not os.access(filepath, os.R_OK):
            print(f"{datetime.now()} - Permission denied for {filepath}")
            return jsonify({"error": "Cannot read data file"}), 403
        
        # Read and validate file
        with open(filepath, 'r') as file:
            data = json.load(file)
            
            # Validate data structure
            if not isinstance(data, list) or len(data) == 0:
                print(f"{datetime.now()} - Invalid data format in file")
                return jsonify({"error": "Invalid data format"}), 500
                
            if 'fake_percent' not in data[0]:
                print(f"{datetime.now()} - Missing required fields")
                return jsonify({"error": "Missing data fields"}), 500
                
        return jsonify(data)
        
    except json.JSONDecodeError:
        print(f"{datetime.now()} - Invalid JSON in file")
        return jsonify({"error": "Corrupted data file"}), 500
    except Exception as e:
        print(f"{datetime.now()} - Unexpected error: {str(e)}")
        return jsonify({"error": "Server error"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)