from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import pickle
from utils import extract_features_from_article
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Dictionary of articles for quick lookup (can be removed or replaced by real DB)
articles = {
    "sample_article": "This is the sample article text to be processed by the feature extraction functions.",
    "https://example.com/article1": "Another article text with some different content."
}

# API route to extract features from article text using pre-defined dictionary
@app.route('/extract_features', methods=['POST'])
def extract_features_route():
    data = request.get_json()
    article_title = data.get("article_title")
    url = data.get("url")

    if article_title and article_title in articles:
        article_text = articles[article_title]
    elif url and url in articles:
        article_text = articles[url]
    else:
        return jsonify({"error": "Article not found."}), 404

    features = extract_features(article_text)
    return jsonify(features)

# Global variable to temporarily store response data
global_resp_data = {}

@app.route('/save_url', methods=['POST'])
def save_url():
    global global_resp_data
    try:
        data = request.get_json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": "Invalid JSON"}), 400

    url = data.get("url") if data else None

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    print(f"THE URL IS {url}")

    def extract_text(url):
        with open("article_text.pkl", "rb") as file:
            d = pickle.load(file)
        return d[url]

    try:
        input_text = extract_text(url)
    except Exception as e:
        return jsonify({"error": f"Failed to extract text for URL: {str(e)}"}), 500

    print(f'Input text (first 30 characters): {input_text[0:30]}')
    f, pred = extract_features_from_article(input_text)
    print("----------------------------------------------------------------------------------------")
    print("EXTRACTED FEATURES:")
    print(f'Model Result: {pred}')

    global_resp_data = [
        {
            "fake_percent": pred * 100,
            "fake_percent_display": "mostly misleading",  # Placeholder text
            "confidence": 10,  # Placeholder value
            "last_updated": datetime.now().isoformat(),
            "polarity_score": round(f['overall_polarity'], 2),
            "subjectivity_score": round(f['overall_subjectivity'], 2),
            "avg_polarity": round(f['avg_sentence_polarity'], 2),
            "avg_subjectivity": round(f['avg_sentence_subjectivity'], 2),
            "num_quotes": round(f['num_speech_attributes'], 0),
            "word_count": round(f['word_count'], 0),
            "flesch_reading_ease": round(f['flesch_reading_ease'], 0)
        }
    ]
    print("----------------------------------------------------------------------------------------")

    return jsonify({"message": "URL processed successfully"})

@app.route('/get_output', methods=['GET'])
def get_output():
    global global_resp_data

    if not global_resp_data:
        return jsonify({"error": "No data available"}), 404

    return jsonify(global_resp_data)

if __name__ == '__main__':
    app.run(debug=True)
