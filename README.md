# OptiWeb — Complete Linux Server Installation & Pro Enhancement Guide

## 🧠 Project Overview

OptiWeb is a **full-stack server monitoring & ML-prediction platform** with two components:

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.1 + Django REST Framework + Celery + MySQL |
| **Frontend** | React 18 + MUI v6 + Recharts + Tailwind CSS |
| **ML Engine** | scikit-learn + pandas + numpy + scipy |
| **Auth** | Token-based (DRF AuthToken) + custom User model |
| **Agent** | Python script pushed to monitored servers |

---

## PART 1 — SERVER INSTALLATION STEPS

### Step 1: Update System & Install Core Packages

```bash
sudo apt update && sudo apt upgrade -y

# Python 3.13, pip, venv
sudo apt install -y python3.13 python3.13-venv python3-pip python3.13-dev

# MySQL (database)
sudo apt install -y mysql-server mysql-client libmysqlclient-dev

# Redis (required for Celery task queue)
sudo apt install -y redis-server

# Node.js 20 LTS (for React frontend)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Nginx (reverse proxy)
sudo apt install -y nginx

# Build tools (needed for mysqlclient C extension)
sudo apt install -y build-essential pkg-config gcc
```

---

### Step 2: Upload & Extract Project

```bash
# Upload your zip to the server, then:
unzip OptiWeb-Code__1_.zip -d /opt/
mv /opt/OptiNew /opt/optiweb
cd /opt/optiweb
```

---

### Step 3: Set Up MySQL Database

```bash
sudo mysql -u root -p
```

Inside MySQL shell:

```sql
CREATE DATABASE optiweb_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'optiweb_user'@'localhost' IDENTIFIED BY 'YourStrongPassword123!';
GRANT ALL PRIVILEGES ON optiweb_db.* TO 'optiweb_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### Step 4: Set Up Python Virtual Environment & Backend

```bash
cd /opt/optiweb/optiweb_backend

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install all Python dependencies
pip install --upgrade pip
pip install django==5.1.* djangorestframework django-cors-headers
pip install mysqlclient
pip install celery redis
pip install scikit-learn pandas numpy scipy
pip install joblib
pip install Pillow   # optional, if image uploads needed
```

---

### Step 5: Configure Backend Settings

Edit `/opt/optiweb/optiweb_backend/optiweb_backend/settings.py`:

```python
# Replace the DEBUG and ALLOWED_HOSTS section:
DEBUG = False   # Set True only during initial setup/testing

ALLOWED_HOSTS = ['YOUR_SERVER_IP', 'yourdomain.com', 'localhost']

# Replace the DATABASES section (add this):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'optiweb_db',
        'USER': 'optiweb_user',
        'PASSWORD': 'YourStrongPassword123!',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Update CORS to allow your frontend:
CORS_ALLOWED_ORIGINS = [
    "http://YOUR_SERVER_IP:3000",
    "https://yourdomain.com",
]

# Static files (for production):
STATIC_ROOT = '/opt/optiweb/static_collected/'
```

---

### Step 6: Run Database Migrations

```bash
cd /opt/optiweb/optiweb_backend
source venv/bin/activate

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # Create admin user
python manage.py collectstatic --noinput
```

---

### Step 7: Test the Django Dev Server

```bash
python manage.py runserver 0.0.0.0:8000
# Visit http://YOUR_SERVER_IP:8000/admin to verify
# Press Ctrl+C when done
```

---

### Step 8: Configure Gunicorn (Production WSGI Server)

```bash
pip install gunicorn

# Test Gunicorn works:
gunicorn optiweb_backend.wsgi:application --bind 0.0.0.0:8000
```

Create a systemd service for the backend:

```bash
sudo nano /etc/systemd/system/optiweb-backend.service
```

Paste:

```ini
[Unit]
Description=OptiWeb Django Backend
After=network.target mysql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/optiweb/optiweb_backend
ExecStart=/opt/optiweb/optiweb_backend/venv/bin/gunicorn \
    optiweb_backend.wsgi:application \
    --workers 4 \
    --bind unix:/run/optiweb-backend.sock \
    --timeout 120
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable optiweb-backend
sudo systemctl start optiweb-backend
sudo systemctl status optiweb-backend
```

---

### Step 9: Configure Celery Worker (for background ML tasks)

```bash
sudo nano /etc/systemd/system/optiweb-celery.service
```

Paste:

```ini
[Unit]
Description=OptiWeb Celery Worker
After=network.target redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/optiweb/optiweb_backend
ExecStart=/opt/optiweb/optiweb_backend/venv/bin/celery \
    -A optiweb_backend worker \
    --loglevel=info \
    --concurrency=2
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable optiweb-celery
sudo systemctl start optiweb-celery
```

---

### Step 10: Set Up React Frontend

```bash
cd /opt/optiweb/optiweb-frontend

# Install dependencies (node_modules included in zip, but re-install cleanly)
rm -rf node_modules
npm install

# Update the API base URL to your server:
# Edit src/services/api.js — change baseURL to your domain/IP
nano src/services/api.js
# Change: baseURL: "http://YOUR_SERVER_IP:8000/"

# Build for production:
npm run build
```

This creates a `build/` folder with the static frontend.

---

### Step 11: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/optiweb
```

Paste:

```nginx
server {
    listen 80;
    server_name YOUR_SERVER_IP yourdomain.com;

    # Serve React frontend
    root /opt/optiweb/optiweb-frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy Django API
    location /api/ {
        proxy_pass http://unix:/run/optiweb-backend.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin/ {
        proxy_pass http://unix:/run/optiweb-backend.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Serve Django static files
    location /static/ {
        alias /opt/optiweb/static_collected/;
        expires 30d;
    }

    # File upload size
    client_max_body_size 50M;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/optiweb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

### Step 12: Fix Permissions

```bash
sudo chown -R www-data:www-data /opt/optiweb/
sudo chmod -R 755 /opt/optiweb/
sudo chmod 775 /opt/optiweb/optiweb_backend/
```

---

### Step 13: (Optional) Enable HTTPS with Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

### Step 14: Enable & Start Redis

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
```

---

### Step 15: Deploy the Monitoring Agent

The agent script lives at `optiweb_backend/static/agent.py`. To deploy on a target server being monitored:

```bash
# On the TARGET server (not the OptiWeb server):
scp /opt/optiweb/optiweb_backend/static/agent.py user@TARGET_SERVER:/opt/optiweb-agent.py

# Edit the config (IP, token):
# config.json backend_api should point to your OptiWeb backend
scp /opt/optiweb/optiweb_backend/static/config.json user@TARGET_SERVER:/opt/config.json

# Run it as a cron job (every minute):
crontab -e
# Add: * * * * * python3 /opt/optiweb-agent.py >> /var/log/optiweb-agent.log 2>&1
```

---

### ✅ Verification Checklist

```bash
# Check all services are running:
sudo systemctl status optiweb-backend optiweb-celery redis-server nginx mysql

# Test the backend API:
curl http://localhost:8000/api/auth/

# Check Django admin:
# Visit http://YOUR_IP/admin
```

---

## PART 2 — PRO-LEVEL ENHANCEMENTS

### 🔐 Security Enhancements

**1. Secure the SECRET_KEY**
```bash
# Generate a new secret key:
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Store it in an environment variable instead of hardcoding:
```python
# settings.py
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-only-for-dev')
```

**2. Add `.env` file support**
```bash
pip install python-dotenv
```
```python
# settings.py top
from dotenv import load_dotenv
load_dotenv()
```

**3. Rate Limiting on Auth Endpoints**
```bash
pip install django-ratelimit
```
Apply the `@ratelimit` decorator to your login view to block brute-force attacks.

---

### ⚡ Performance Enhancements

**1. Add Database Connection Pooling**
```bash
pip install django-db-connection-pool
```

**2. Cache API Responses with Redis**
```python
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```
Decorate slow views with `@cache_page(60 * 5)` for a 5-minute cache.

**3. Add Gzip Compression in Nginx**
```nginx
# In your nginx config, inside http {}:
gzip on;
gzip_types text/plain application/json application/javascript text/css;
gzip_min_length 1000;
```

---

### 📊 Feature Enhancements

**1. WebSocket Real-Time Monitoring**

Replace polling with live server metrics using Django Channels:
```bash
pip install channels channels-redis daphne
```
Update `INSTALLED_APPS` to include `'channels'` and `'daphne'`, configure `CHANNEL_LAYERS` with Redis, and switch `ASGI_APPLICATION` to point to a routing config.

**2. ML Model Auto-Retraining Pipeline**

The project already has `ml_api/retrain_model.py`. Automate it with Celery Beat:
```bash
pip install django-celery-beat
```
Add to `INSTALLED_APPS`, run `python manage.py migrate`, and schedule retraining jobs via Django admin under Periodic Tasks.

**3. Email Alerting**

Tie into the existing `ml_api/alerts.py` and send real alerts via SMTP:
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
```

**4. Structured Logging**

```bash
pip install structlog
```
Replace bare `print()` calls with structured JSON logs, enabling easier debugging and log aggregation.

---

### 🚀 DevOps / Deployment Enhancements

**1. Docker Compose (Recommended for Easy Deployment)**

Create a `docker-compose.yml` that packages Django, Celery, MySQL, Redis, and Nginx together — making the entire stack deployable with a single `docker-compose up -d`.

**2. Automated Backups**
```bash
# Daily MySQL backup cron job:
0 2 * * * mysqldump -u optiweb_user -pYourPassword optiweb_db > /opt/backups/optiweb_$(date +\%Y\%m\%d).sql
```

**3. Health-Check Endpoint**

Add a simple `/api/health/` endpoint returning `{"status": "ok", "db": true, "cache": true}` — useful for load balancers and uptime monitors.

**4. Monitoring OptiWeb Itself**

Set up an external uptime check (UptimeRobot, BetterStack, or similar) pointing at your `/api/health/` endpoint to get alerts if OptiWeb itself goes down.

---

### 🎨 Frontend Enhancements

**1. Environment Variables**
```bash
# Create .env in optiweb-frontend/
REACT_APP_API_URL=https://yourdomain.com
```
Then in `api.js`:
```js
baseURL: process.env.REACT_APP_API_URL
```

**2. Progressive Web App (PWA)**

Create React App already has PWA support built in. Register the service worker in `index.js` to enable offline functionality and add-to-homescreen.

**3. Dark Mode Toggle**

MUI v6 supports a `useColorScheme` hook natively — add a toggle to the existing Navbar for instant dark/light switching.

**4. Dashboard Export to PDF/CSV**

Add `react-pdf` or `file-saver` + `xlsx` to let admins export monitoring data and ML prediction reports.

---

## Quick Reference: All Services

| Service | Command |
|---------|---------|
| Start all | `sudo systemctl start optiweb-backend optiweb-celery redis-server nginx` |
| View backend logs | `sudo journalctl -u optiweb-backend -f` |
| View Celery logs | `sudo journalctl -u optiweb-celery -f` |
| Restart after code change | `sudo systemctl restart optiweb-backend` |
| Django shell | `cd /opt/optiweb/optiweb_backend && source venv/bin/activate && python manage.py shell` |
| Run migrations | `python manage.py migrate` |
| Rebuild frontend | `cd /opt/optiweb/optiweb-frontend && npm run build` |
