from sqlalchemy import create_engine
import pandas as pd
import os
import urllib.parse

# ? Database Connection Settings
DB_USER = "optiweb_user"
DB_PASS = "20171228@Opti"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "optiweb_db"

# ? Encode password for MySQL connection
DB_PASS_ENCODED = urllib.parse.quote_plus(DB_PASS)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ? Create database connection
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# ? Query to fetch the latest 5000 server metrics
query = """
SELECT server_id, cpu_usage, memory_usage, disk_usage, uptime, 
       web_service_status, db_service_status, logs, timestamp 
FROM agent_monitoring_servermetrics
ORDER BY timestamp DESC
LIMIT 5000;
"""

# ? Load data into Pandas DataFrame
df_new = pd.read_sql(query, engine)

# ? Check if historical data file exists
historical_data_path = "enhanced_server_metrics_data.csv"
if os.path.exists(historical_data_path):
    df_old = pd.read_csv(historical_data_path)
    
    # ? Append new data while preventing duplicates
    df_combined = pd.concat([df_old, df_new]).drop_duplicates(subset=['server_id', 'timestamp'], keep="last")
else:
    df_combined = df_new

# ? Save updated data
df_combined.to_csv(historical_data_path, index=False)
print("? Data successfully extracted and updated in 'enhanced_server_metrics_data.csv'")
