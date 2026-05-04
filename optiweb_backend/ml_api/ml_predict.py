import joblib
import numpy as np
import os

# Load enhanced trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "enhanced_failure_predictor_model.pkl")
model = joblib.load(MODEL_PATH)

def predict_failure(features):
    """
    Predicts service failure risk based on enhanced server metrics.
    :param features: List of feature values (same as in training)
    :return: Tuple (failure_risk: bool, reasons: list)
    """
    input_data = np.array([features])
    prediction = model.predict(input_data)
    failure_risk = bool(prediction[0])

    # Reasons logic
    reasons = []
    if features[0] > 85:
        reasons.append("High CPU usage")
    if features[1] > 90:
        reasons.append("High memory usage")
    if features[2] > 95:
        reasons.append("High disk usage")
    if features[4] > 5:
        reasons.append("Multiple 500 Internal Server Errors")
    if features[9] > 3:
        reasons.append("Database connection failures detected")

    return failure_risk, reasons
