import psutil
import os
import requests
import platform
import time
import json
import subprocess

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from a JSON file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("? Error: Config file not found.")
        return {}
    except json.JSONDecodeError:
        print("? Error: Invalid JSON format in config file.")
        return {}

config = load_config()
BACKEND_API = config.get("backend_api", "http://203.143.13.21:8000/api/auth/metrics/")
AUTOFIX_API = config.get("automation_api", "http://203.143.13.21:8000/api/automation/fix_issue/")
SERVER_IP = config.get("web_server_ip", "")
TOKEN = config.get("token", "")

if not SERVER_IP or not TOKEN:
    print("? Error: Missing server IP or authentication token in config file.")
    exit(1)

def collect_server_metrics():
    """Collect system metrics."""
    return {
        "server_id": SERVER_IP,
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "uptime": int(time.time() - psutil.boot_time()),
    }

def is_service_installed(service_name):
    """Check if a service is installed by verifying its systemd unit file exists."""
    check_cmd = f"systemctl list-unit-files | grep -E '^{service_name}.service'"
    try:
        result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
        return bool(result.stdout.strip())
    except Exception:
        return False

def check_service_status(service_name):
    """Check if an installed service is active or inactive."""
    if not is_service_installed(service_name):
        return None  # Ignore if service is not installed
    
    try:
        result = subprocess.run(["systemctl", "is-active", service_name], capture_output=True, text=True)
        status = result.stdout.strip()
        return status if status in ["active", "inactive"] else None
    except Exception:
        return None

def detect_installed_services():
    """Detect only installed web and database services and their statuses."""
    service_list = ["apache2", "nginx", "mysql", "postgresql"]
    installed_services = {}

    for service in service_list:
        status = check_service_status(service)
        if status:  # Only add installed services
            installed_services[service] = status

    return installed_services

def collect_error_logs():
    """Collect critical error logs from system and services."""
    logs = []
    
    try:
        # Collect system errors (journalctl for systemd)
        logs.extend(subprocess.run(["journalctl", "-p", "3..4", "-n", "50"], capture_output=True, text=True).stdout.splitlines())

        # Fetch logs from system files
        log_paths = ["/var/log/syslog", "/var/log/messages"]
        for log_path in log_paths:
            if os.path.exists(log_path):
                with open(log_path, "r") as log_file:
                    logs.extend(log_file.readlines()[-50:])

        # Web & Database Service Logs
        service_logs = {
            "apache2": "/var/log/apache2/error.log",
            "nginx": "/var/log/nginx/error.log",
            "mysql": "/var/log/mysql/error.log",
            "postgresql": "/var/log/postgresql/postgresql.log",
        }

        for service, log_path in service_logs.items():
            if os.path.exists(log_path):
                with open(log_path, "r") as log_file:
                    logs.extend(log_file.readlines()[-50:])

    except Exception as e:
        logs.append(f"? Error collecting logs: {e}")

    return logs[-50:]  # Limit logs to last 50 lines

def restart_service(service_name):
    """Attempt to restart a service if it's down."""
    try:
        result = subprocess.run(["systemctl", "restart", service_name], capture_output=True, text=True)
        if result.returncode == 0:
            return f"? {service_name} restarted successfully."
        return f"? Failed to restart {service_name}."
    except Exception as e:
        return f"? Error restarting {service_name}: {str(e)}"

def resolve_issues(installed_services):
    """Automatically attempt to fix detected issues."""
    auto_fixes = {}

    for service, status in installed_services.items():
        if status == "inactive":
            auto_fixes[service] = restart_service(service)

    return auto_fixes

def send_automation_log(fixes):
    """Send automation logs to the backend API."""
    payload = {
        "server_id": SERVER_IP,
        "fixes": json.dumps(fixes)
    }

    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(AUTOFIX_API, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print("Automation logs sent successfully.")
        else:
            print(f"Error sending automation logs: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Error sending automation logs: {e}")

def send_data_to_backend(metrics, logs, installed_services):
    """Send collected data to the backend API with authentication."""
    web_services = {k: v for k, v in installed_services.items() if k in ["apache2", "nginx"]}
    db_services = {k: v for k, v in installed_services.items() if k in ["mysql", "postgresql"]}

    payload = {
        "server_id": SERVER_IP,
        "cpu_usage": metrics["cpu_usage"],
        "memory_usage": metrics["memory_usage"],
        "disk_usage": metrics["disk_usage"],
        "uptime": metrics["uptime"],
        "logs": json.dumps(logs),  # Send filtered logs
        "web_service_status": json.dumps(web_services),
        "db_service_status": json.dumps(db_services),
    }

    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(BACKEND_API, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Error sending data: {e}")

def main():
    while True:
        metrics = collect_server_metrics()
        logs = collect_error_logs()
        installed_services = detect_installed_services()
        
        # Send server metrics
        send_data_to_backend(metrics, logs, installed_services)
        
        # Perform automatic issue resolution
        fixes = resolve_issues(installed_services)
        if fixes:
            send_automation_log(fixes)

        time.sleep(60)

if __name__ == "__main__":
    main()
