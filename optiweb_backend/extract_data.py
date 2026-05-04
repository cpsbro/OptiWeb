import pandas as pd
import numpy as np
import os
import pymysql
from sqlalchemy import create_engine

# Database connection details (Update accordingly)
DB_USER = "optiweb_user"
DB_PASSWORD = "20171228@Opti"
DB_HOST = "localhost"
DB_NAME = "optiweb_db"

# Connect to the database
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# Fetch latest metrics (past 7 days)
query = """
SELECT server_id, cpu_usage, memory_usage, disk_usage, uptime, web_service_status, 
       db_service_status, logs, timestamp
FROM agent_monitoring_servermetrics
WHERE timestamp >= NOW() - INTERVAL 7 DAY
ORDER BY timestamp DESC;
"""

print("í ½í´„ Fetching latest weekly data from database...")
df = pd.read_sql(query, engine)

if df.empty:
    print("âš ï¸ No data found for the past 7 days!")
    exit()

# Function to simulate log-based features
def add_log_features(df):
    np.random.seed(42)

    # Add new log-related features
    df['web_500_errors'] = np.random.poisson(1, len(df))
    df['web_404_errors'] = np.random.poisson(2, len(df))
    df['web_ssl_errors'] = np.random.binomial(1, 0.1, len(df))
    df['web_slow_response_warnings'] = np.random.poisson(1, len(df))
    df['web_resource_limit_warnings'] = np.random.binomial(1, 0.2, len(df))
    df['db_connection_failures'] = np.random.poisson(1, len(df))
    df['db_auth_failures'] = np.random.binomial(1, 0.05, len(df))
    df['db_deadlocks'] = np.random.poisson(0.5, len(df))
    df['db_out_of_memory'] = np.random.binomial(1, 0.03, len(df))
    df['db_slow_queries'] = np.random.poisson(2, len(df))
    df['db_connection_limits'] = np.random.binomial(1, 0.1, len(df))

    # Create log-based risk
    df['log_based_risk'] = (df['web_500_errors'] + df['db_out_of_memory'] + df['db_connection_failures']) > 2

    # Ensure 'service_failure_risk' exists, or create it
    if 'service_failure_risk' not in df.columns:
        df['service_failure_risk'] = False  # Initialize with False if missing

    # Combine existing service_failure_risk with log_based_risk
    df['service_failure_risk'] = df['service_failure_risk'] | df['log_based_risk']

    return df

# Apply log feature enhancements
df = add_log_features(df)

# Delete old dataset
dataset_path = "enhanced_server_metrics_data.csv"
if os.path.exists(dataset_path):
    os.remove(dataset_path)
    print("í ½í·‘ï¸ Deleted old dataset.")

# Save new dataset
df.to_csv(dataset_path, index=False)
print("âœ… New dataset saved as 'enhanced_server_metrics_data.csv'")
