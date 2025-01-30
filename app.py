import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Load the models
models = {}
model_names = ['logreg', 'knn', 'svm', 'rf', 'nb']

for model_name in model_names:
    with open(f'{model_name}_model.pkl', 'rb') as f:
        models[model_name] = pickle.load(f)

# Load the scaler
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Define Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Define Prediction Route
@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        data = request.json  # Get input JSON

        # Extract features from incoming data
        incoming_data = data["data"]

        # List of features used during training (ensure this matches your training data's columns)
        required_features = ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PIRATIO"]

        # Only keep the required features in the incoming data
        filtered_data = {key: value for key, value in incoming_data.items() if key in required_features}

        if len(filtered_data) != len(required_features):
            return jsonify({"error": "Missing required features in the input data."}), 400

        # Get the features as a list and ensure they're floats
        features = list(filtered_data.values())
        features = [float(x) for x in features]  # Ensure it's a list of floats
        X_test = np.array(features).reshape(1, -1)

        # Apply Scaling (only scaling, no PCA)
        X_test_scaled = scaler.transform(X_test)

        # Make predictions
        predictions = {model: models[model].predict(X_test_scaled).tolist() for model in models}

        return jsonify(predictions)
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
