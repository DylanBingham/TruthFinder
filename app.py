import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/save_url', methods=['POST'])
def save_url():
    print("Request received!")  # Debugging: Confirm request hit the endpoint

    try:
        data = request.get_json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": "Invalid JSON"}), 400

    print("Parsed JSON:", data)  # Debugging: Print received JSON data

    url = data.get("url") if data else None

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    with open("input_url.txt", "w") as file:
        file.write(url)

    print(f"URL saved: {url}")  # Debugging: Confirm the write action

    return jsonify({"message": "URL saved successfully"})


# New endpoint to serve output data
@app.route('/get_output', methods=['GET'])
def get_output():
    try:
        with open("output_data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        print("Error reading output_data.json:", e)
        return jsonify({"error": "Unable to read output data"}), 500


if __name__ == '__main__':
    app.run(debug=True)
