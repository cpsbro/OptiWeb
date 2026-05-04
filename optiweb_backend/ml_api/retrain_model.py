import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# ? Load the latest enhanced dataset
data_path = "enhanced_server_metrics_data.csv"
if not os.path.exists(data_path):
    print("? No dataset found for training.")
    exit(1)

data = pd.read_csv(data_path)

# ? Ensure the 'service_failure_risk' column exists
if "service_failure_risk" not in data.columns:
    print("? 'service_failure_risk' column missing in dataset. Cannot proceed with training.")
    exit(1)

# ? Handle Missing Values in Target Column
data["service_failure_risk"] = data["service_failure_risk"].fillna(0).astype(int)  # Fill NaN with 0 (Low risk)

# ? Features & Target
features = [
    'cpu_usage', 'memory_usage', 'disk_usage', 'uptime',
    'web_500_errors', 'web_404_errors', 'web_ssl_errors',
    'web_slow_response_warnings', 'web_resource_limit_warnings',
    'db_connection_failures', 'db_auth_failures', 'db_deadlocks',
    'db_out_of_memory', 'db_slow_queries', 'db_connection_limits'
]
target = 'service_failure_risk'

# ? Ensure required features exist
for feature in features:
    if feature not in data.columns:
        print(f"? Missing feature: {feature} in dataset. Skipping training.")
        exit(1)

# ? Prepare the dataset
X = data[features].fillna(0)  # Replace NaN values with 0 in feature columns
y = data[target]

# ? Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ? Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ? Evaluate Model
y_pred = model.predict(X_test)
print("? Model Training Complete!")
print(classification_report(y_test, y_pred))
print(f"? Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# ? Delete old model if exists
model_path = "enhanced_failure_predictor_model.pkl"
if os.path.exists(model_path):
    os.remove(model_path)

# ? Save new model
joblib.dump(model, model_path)
print("? Trained model saved as 'enhanced_failure_predictor_model.pkl'")
