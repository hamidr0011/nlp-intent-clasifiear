from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

MODEL_FILE = "model.pkl"
model = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model():
    global model
    if os.path.exists(MODEL_FILE):
        try:
            logger.info("Loading model...")
            model = joblib.load(MODEL_FILE)
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
    else:
        logger.error(f"Model file '{MODEL_FILE}' not found. Please run train.py first.")

load_model()

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field in JSON request'}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({'error': 'Empty text provided'}), 400

    try:
        intent = model.predict([text])[0]
        max_prob = None
        
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba([text])[0]
            max_prob = float(max(probs))
            
        return jsonify({
            'intent': intent,
            'confidence': max_prob
        })
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
