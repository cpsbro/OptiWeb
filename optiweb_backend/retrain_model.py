import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the enhanced dataset
data = pd.read_csv('enhanced_server_metrics_data.csv')

# Features to use for training (including log-based features)
features = [
    'cpu_usage', 'memory_usage', 'disk_usage', 'uptime',
    'web_500_errors', 'web_404_errors', 'web_ssl_errors',
    'web_slow_response_warnings', 'web_resource_limit_warnings',
    'db_connection_failures', 'db_auth_failures', 'db_deadlocks',
    'db_out_of_memory', 'db_slow_queries', 'db_connection_limits'
]

# Target variable
target = 'service_failure_risk'

# Prepare the dataset
X = data[features]
y = data[target].astype(int)  # Ensure target is in numeric format

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("? Model Training Complete!")
print("?? Classification Report:")
print(classification_report(y_test, y_pred))
print(f"?? Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Save the trained model
joblib.dump(model, 'enhanced_failure_predictor_model.pkl')
print("?? Trained model saved as 'enhanced_failure_predictor_model.pkl'")
