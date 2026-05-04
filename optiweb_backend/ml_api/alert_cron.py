import requests

# ? API Endpoint
API_URL = "http://127.0.0.1:8000/api/ml/predict/"

# ? Dummy Data for Prediction
data = {
    "cpu_usage": 92, "memory_usage": 95, "disk_usage": 90, "uptime": 5000,
    "web_500_errors": 3, "web_404_errors": 0, "web_ssl_errors": 1,
    "web_service_status": "{\"apache2\": \"inactive\"}", 
    "db_service_status": "{\"mysql\": \"inactive\"}",
}

# ? Send POST request
response = requests.post(API_URL, json=data)

print(f"? AI Prediction Triggered: {response.json()}")
