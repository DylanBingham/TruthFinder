from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import pickle
from utils import extract_features_from_article
import datetime
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


global_resp_data = {}
# Your existing API routes
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


    return jsonify({"message": "URL saved successfully"})

@app.route('/get_output', methods=['GET'])

def get_output():
    global global_resp_data  # Access global variable

    if not global_resp_data:
        return jsonify({"error": "No data available"}), 404

    data = global_resp_data  # Use the stored data
    return jsonify(data)
    
if __name__ == '__main__':
    app.run(debug=True)