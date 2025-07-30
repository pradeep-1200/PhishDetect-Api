from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # pyright: ignore[reportMissingModuleSource]
import joblib # pyright: ignore[reportMissingImports]
import os
from utils import extract_features

app = Flask(__name__)
CORS(app)

# Load trained model with correct path
model_path = os.path.join(os.path.dirname(__file__), 'phishing_model.pkl')
model = joblib.load(model_path)

@app.route('/')
def home():
    return "✅ PhishDetectAI API is running!"

@app.route('/predict-url', methods=['POST'])
def predict_url():
    data = request.json
    try:
        if 'url' not in data:
            return jsonify({'error': 'Missing URL'}), 400

        url = data['url']
        features = extract_features(url)

        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]

        result = {
            'prediction': int(prediction),
            'confidence': round(float(max(probability)) * 100, 2)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render provides this PORT
    app.run(host='0.0.0.0', port=port, debug=True)  