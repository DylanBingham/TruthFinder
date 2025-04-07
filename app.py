from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
<<<<<<< HEAD
import os
import json
import pickle
from utils import extract_features_from_article
import datetime
from datetime import datetime
app = Flask(__name__)
CORS(app)

=======
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

>>>>>>> origin/dev
# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

<<<<<<< HEAD
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


global_resp_data = {}
# Your existing API routes
@app.route('/save_url', methods=['POST'])
def save_url():
    global global_resp_data
=======
# Your existing API routes
@app.route('/save_url', methods=['POST'])
def save_url():
>>>>>>> origin/dev
    try:
        data = request.get_json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": "Invalid JSON"}), 400

    url = data.get("url") if data else None
<<<<<<< HEAD
  
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    print(f"THE URL IS {url}")
    def extract_text(url):
        with open("article_text.pkl", "rb") as file:
            d = pickle.load(file)
        return d[url]
    input_text = extract_text(url)
    print(f'Input text (first 30 characters) is {input_text[0:30]}')
    f,pred = extract_features_from_article(input_text)
    print("----------------------------------------------------------------------------------------")
    print("EXTRACTED FEATURES:----------------------------------------------------------------------------------------")
    
    
    print(f'Model Result: {pred}')
    
    global_resp_data = [
        {
            "fake_percent": pred*100,  
            "fake_percent_display": "mostly misleading", #Write some python algorithm that calculates this
            "confidence": 10, #See if you can write some kind of python algorithm to figure this out, though this may be more backedn than front end work. 
            "last_updated": datetime.now().isoformat(),
            "polarity_score": round(f['overall_polarity'],2),
            "subjectivity_score": round(f['overall_subjectivity'],2),
            "avg_polarity": round(f['avg_sentence_polarity'],2),
            "avg_subjectivity": round(f['avg_sentence_subjectivity'],2),  # Replace with actual calculation if available
            "num_quotes": round(f['num_speech_attributes'],0),
            "word_count": round(f['word_count'],0),
            "flesch_reading_ease": round(f['flesch_reading_ease'],0)
        }
    ]
    print("----------------------------------------------------------------------------------------")

=======
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    with open("input_url.txt", "w") as file:
        file.write(url)
>>>>>>> origin/dev

    return jsonify({"message": "URL saved successfully"})

@app.route('/get_output', methods=['GET'])
<<<<<<< HEAD

def get_output():
    global global_resp_data  # Access global variable

    if not global_resp_data:
        return jsonify({"error": "No data available"}), 404

    data = global_resp_data  # Use the stored data
    return jsonify(data)
=======
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
>>>>>>> origin/dev
    
if __name__ == '__main__':
    app.run(debug=True)