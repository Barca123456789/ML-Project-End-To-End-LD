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

        # Map the incoming feature names to the model's expected feature names
        feature_mapping = {
            "Total Bilirubin": "Total_Bilirubin",
            "Direct Bilirubin": "Direct_Bilirubin",
            "Alkaline Phosphatase": "Alkaline_Phosphotase",
            "Alanine Aminotransferase": "Alamine_Aminotransferase",
            "Aspartate Aminotransferase": "Aspartate_Aminotransferase",
            "Total Proteins": "Total_Protiens",
            "Albumin and Globulin Ratio": "Albumin_and_Globulin_Ratio"
        }

        # Normalize incoming data keys to match the model's expected feature names
        incoming_data = data["data"]
        normalized_data = {}

        for key, value in incoming_data.items():
            # Check if the feature is present in the mapping
            if key in feature_mapping:
                normalized_data[feature_mapping[key]] = value
            else:
                normalized_data[key] = value

        # Ensure that all required features are in the normalized data
        required_features = [
            "Age", "Total_Bilirubin", "Direct_Bilirubin", "Alkaline_Phosphotase", 
            "Alamine_Aminotransferase", "Aspartate_Aminotransferase", "Total_Protiens", 
            "Albumin", "Albumin_and_Globulin_Ratio"
        ]

        if not all(feature in normalized_data for feature in required_features):
            return jsonify({"error": "Missing required features in the input data."}), 400

        # Extract and convert features to float
        features = [
            float(normalized_data["Age"]),
            float(normalized_data["Total_Bilirubin"]),
            float(normalized_data["Direct_Bilirubin"]),
            float(normalized_data["Alkaline_Phosphotase"]),
            float(normalized_data["Alamine_Aminotransferase"]),
            float(normalized_data["Aspartate_Aminotransferase"]),
            float(normalized_data["Total_Protiens"]),
            float(normalized_data["Albumin"]),
            float(normalized_data["Albumin_and_Globulin_Ratio"])
        ]

        # Process gender (1 for Female, 0 for Male)
        if "Gender" in normalized_data:
            gender = normalized_data["Gender"]
            gender_female = 1 if gender == "Female" else 0
            features.append(gender_female)  # Only append one gender feature
        else:
            return jsonify({"error": "Gender data missing."}), 400

        # Convert features into numpy array and reshape for prediction
        X_test = np.array(features).reshape(1, -1)

        # Apply scaling
        X_test_scaled = scaler.transform(X_test)

        # Convert numerical predictions into labels
        label_mapping = {1: "No Liver Disease", 2: "Liver Disease"}

        # Make predictions using all models and map to readable labels
        predictions = {
            model: label_mapping.get(models[model].predict(X_test_scaled)[0], "Unknown")
            for model in models
        }

        return jsonify(predictions)

    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)

