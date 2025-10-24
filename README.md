<div align="center">

![Cookie Scanner Logo](https://via.placeholder.com/200x80/4F46E5/FFFFFF?text=Cookie+Scanner)

**🍪 A world-class cookie scanning platform that competes with CookieYes and Termly. Built with FastAPI, React, PostgreSQL, Redis, and Playwright for comprehensive website cookie analysis.**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/AGILAN2005/cookie-scanner/blob/main/LICENSE)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)

[📖 Documentation](README.md) • [🐛 Report Bug](https://github.com/AGILAN2005/cookie-scanner/issues) • [✨ Request Feature](https://github.com/AGILAN2005/cookie-scanner/issues)

</div>

---

## 📋 Table of Contents
* [Features](#-features)
* [Architecture](#-architecture)
* [Tech Stack](#-tech-stack)
* [Prerequisites](#-prerequisites)
* [Quick Start](#-quick-start-docker---recommended)
* [Manual Setup](#️-manual-setup-without-docker)
* [Configuration](#️-configuration)
* [Usage Guide](#-usage-guide)
* [API Documentation](#-api-documentation)
* [Troubleshooting](#-troubleshooting)
* [Development](#-development)
* [Contributing](#-contributing)
* [License](#-license)
* [Support](#-support)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔍 **Comprehensive Scanning**
- **Full-Site Crawling**: Scans entire websites, not just single pages
- **Consent Banner Detection**: Automatically interacts with cookie consent popups
- **Broad Analysis**: Tracks cookies, localStorage, and sessionStorage
- **Page-Level Tracking**: Detailed metadata for each scanned page

</td>
<td width="50%">

### 🤖 **Intelligent Analysis**
- **AI-Powered Enrichment**: Uses Google Gemini to categorize unknown cookies
- **GDPR/CCPA Compliance**: Generates compliance insights and recommendations
- **Persistent Knowledge Base**: Learns and stores cookie information
- **Concurrent Scanning**: Efficient multi-page scanning

</td>
</tr>
</table>

---

## 🏗️ Architecture
```

cookie-scanner/
├── frontend/                  \# React frontend application
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── backend/                  \# FastAPI backend application
│   ├── main.py               \# API endpoints
│   ├── worker.py             \# Celery background tasks
│   ├── scanner.py            \# Playwright cookie scanner
│   ├── enrichment.py         \# AI-powered cookie enrichment
│   ├── models.py             \# Database models
│   ├── database.py           \# Database configuration
│   ├── patterns.py           \# Known cookie patterns
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── docker-compose.yml         \# Docker orchestration
└── README.md

````

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technologies |
|:-----:|:------------|
| **Frontend** | ![React](https://img.shields.io/badge/-React-20232A?style=for-the-badge&logo=react) ![Vite](https://img.shields.io/badge/-Vite-646CFF?style=for-the-badge&logo=vite) ![Nginx](https://img.shields.io/badge/-NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white) |
| **Backend** | ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=for-the-badge&logo=fastapi) ![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) |
| **Cache & Queue** | ![Redis](https://img.shields.io/badge/-Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white) ![Celery](https://img.shields.io/badge/-Celery-3AA655?style=for-the-badge&logo=celery&logoColor=white) |
| **Scanner** | ![Playwright](https://img.shields.io/badge/-Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white) |
| **AI** | ![Google Gemini](https://img.shields.io/badge/-Google_Gemini-8E77F0?style=for-the-badge&logo=google-gemini&logoColor=white) |
| **DevOps** | ![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |

</div>

---

## 📦 Prerequisites

**For Docker Setup (Recommended)**
* Docker Desktop 20.10+ or Docker Engine 20.10+
* Docker Compose 2.0+
* 8GB RAM minimum (16GB recommended)
* 10GB free disk space

**For Manual Setup**
* Python 3.11+
* Node.js 20+
* PostgreSQL 15+
* Redis 7+
* Google API Key (for AI enrichment)

---

## 🚀 Quick Start (Docker - Recommended)

**1. Clone the Repository**
```bash
git clone [https://github.com/AGILAN2005/cookie-scanner.git](https://github.com/AGILAN2005/cookie-scanner.git)
cd cookie-scanner
````

**2. Configure Environment Variables**
Create a `.env` file in the `backend_kritesh/` directory:

```bash
cd backend_kritesh
cat > .env << EOF
DATABASE_URL="postgresql://admin:admin123@postgresql:5432/cookie_consent_db"
REDIS_URL="redis://redis:6379/0"
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
GEMINI_MODEL="gemini-2.5-flash"
COOKIE_DB_PATH="exhaustive_cookie_database.json"
EOF
cd ..
```

⚠️ **Important**: Replace `YOUR_GOOGLE_API_KEY_HERE` with your actual Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

**3. Build and Start All Services**

```bash
# Build all Docker images (first time only)
docker-compose build

# Start all services in detached mode
docker-compose up -d
```

This will start:

  * **PostgreSQL** on port `5433`
  * **Redis** on port `6381`
  * **Backend API** on port `8001`
  * **Celery Worker** (background job processor)
  * **Frontend** on port `3000`

**4. Initialize the Database**

```bash
# Run database initialization script
docker-compose exec backend python init_db.py
```

**5. Verify Services**
Check if all services are running:

```bash
docker-compose ps
```

Expected output:

```
NAME                          STATUS    PORTS
cookie_scanner_backend        Up        0.0.0.0:8001->8000/tcp
cookie_scanner_db             Up        0.0.0.0:5433->5432/tcp
cookie_scanner_frontend       Up        0.0.0.0:3000->80/tcp
cookie_scanner_redis          Up        0.0.0.0:6381->6379/tcp
cookie_scanner_worker         Up
```

**6. Access the Application**

  * **Frontend**: `http://localhost:3000`
  * **Backend API**: `http://localhost:8001`
  * **API Documentation**: `http://localhost:8001/docs`
  * **Health Check**: `http://localhost:8001/health`

-----

## 🛠️ Manual Setup (Without Docker)

**Backend Setup**

1.  **Install System Dependencies**

      * **Ubuntu/Debian**:
        ```bash
        sudo apt-get update
        sudo apt-get install -y postgresql-15 redis-server python3.11 python3.11-venv
        ```
      * **macOS**:
        ```bash
        brew install postgresql@15 redis python@3.11
        ```

2.  **Setup PostgreSQL Database**

    ```bash
    # Start PostgreSQL
    sudo systemctl start postgresql  # Linux
    brew services start postgresql@15  # macOS

    # Create database and user
    sudo -u postgres psql
    ```

    In PostgreSQL shell:

    ```sql
    CREATE DATABASE cookie_consent_db;
    CREATE USER admin WITH PASSWORD 'admin123';
    GRANT ALL PRIVILEGES ON DATABASE cookie_consent_db TO admin;
    \q
    ```

3.  **Setup Backend Environment**

    ```bash
    cd backend

    # Create virtual environment
    python3.11 -m venv venv

    # Activate virtual environment
    source venv/bin/activate  # Linux/macOS
    # OR
    venv\Scripts\activate  # Windows

    # Upgrade pip
    pip install --upgrade pip

    # Install dependencies
    pip install -r requirements.txt

    # Install Playwright browsers
    playwright install chromium
    playwright install-deps chromium
    ```

4.  **Configure Backend**
    Create `.env` file:

    ```bash
    cat > .env << EOF
    DATABASE_URL="postgresql://admin:admin123@localhost:5432/cookie_consent_db"
    REDIS_URL="redis://localhost:6379/0"
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    GEMINI_MODEL="gemini-2.5-flash"
    COOKIE_DB_PATH="exhaustive_cookie_database.json"
    EOF
    ```

5.  **Initialize Database**

    ```bash
    python init_db.py
    ```

6.  **Start Backend Services**

      * **Terminal 1 - API Server**:
        ```bash
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ```
      * **Terminal 2 - Celery Worker**:
        ```bash
        celery -A worker.celery_app worker --loglevel=info --concurrency=2
        ```
      * **Terminal 3 - Redis (if not running as service)**:
        ```bash
        redis-server
        ```

**Frontend Setup**

1.  **Install Node.js Dependencies**

    ```bash
    cd frontend
    npm install
    ```

2.  **Configure Frontend**
    Create or update `.env` file:

    ```bash
    cat > .env << EOF
    REACT_APP_API_URL=http://localhost:8000
    REACT_APP_ENV=development
    EOF
    ```

3.  **Start Frontend Development Server**

    ```bash
    npm run dev
    ```

    The frontend will be available at `http://localhost:5173` (Vite default) or `http://localhost:3000`.

-----

## ⚙️ Configuration

**Environment Variables**

*Backend (`.env` in `backend/`)*

```bash
# Database Configuration
DATABASE_URL="postgresql://admin:admin123@localhost:5432/cookie_consent_db"

# Redis Configuration
REDIS_URL="redis://localhost:6379/0"

# Google AI Configuration
GOOGLE_API_KEY="your-api-key-here"
GEMINI_MODEL="gemini-2.5-flash"

# Cookie Database
COOKIE_DB_PATH="exhaustive_cookie_database.json"

# Optional: Scanning Configuration
SCAN_TIMEOUT=60
MAX_CONCURRENT_SCANS=3
BROWSER_HEADLESS=true
```

*Frontend (`.env` in `frontend/`)*

```bash
# API URL
REACT_APP_API_URL=http://localhost:8001

# Environment
REACT_APP_ENV=production
GENERATE_SOURCEMAP=false
```

**Docker Compose Configuration**
You can customize ports and resources in `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change 8001 to your preferred port
    environment:
      WORKERS: 2  # Increase for more concurrency
```

-----

## 📖 Usage Guide

**1. Scanning a Website**

*Via Web Interface*

1.  Navigate to `http://localhost:3000`
2.  Click "Add New Site" or "Start Scan"
3.  Enter the website URL (e.g., `https://example.com`)
4.  Fill in site details:
      * **Type**: `ROOT`, `SUBPAGE`, or `CUSTOM`
      * **Version**: Website version identifier
      * **Owner Name**: Site owner's name
      * **Owner Email**: Contact email
5.  Configure scan options:
      * **Accept Consent**: Auto-click cookie banners
      * **Wait Seconds**: Time to wait for cookies (default: 3s)
      * **Max Pages**: Maximum pages to crawl (default: 20)
      * **Deep Scroll**: Enable page scrolling (slower but more thorough)
6.  Click "Start Scan"

*Via API*

cURL Example:

```bash
curl -X POST http://localhost:8001/scan \
  -H "Content-Type: application/json" \
  -d '{
    "url": "[https://example.com](https://example.com)",
    "type": "ROOT",
    "version": "1.0",
    "ownerName": "John Doe",
    "ownerEmail": "john@example.com",
    "options": {
      "accept_consent": true,
      "wait_seconds": 3,
      "max_pages": 20,
      "deep_scroll": false
    }
  }'
```

Python Example:

```python
import requests

response = requests.post('http://localhost:8001/scan', json={
    "url": "[https://example.com](https://example.com)",
    "type": "ROOT",
    "version": "1.0",
    "ownerName": "John Doe",
    "ownerEmail": "john@example.com",
    "options": {
        "accept_consent": True,
        "wait_seconds": 3,
        "max_pages": 20,
        "deep_scroll": False
    }
})

job = response.json()
print(f"Job ID: {job['job_id']}")
print(f"Status: {job['status']}")
```

**2. Checking Scan Status**

```bash
# Get job status
curl http://localhost:8001/status/{job_id}
```

**3. Retrieving Scan Results**

```bash
# Get complete scan results
curl http://localhost:8001/result/{job_id}
```

**4. Managing Sites**

```bash
# List all sites
curl http://localhost:8001/sites

# Update site details
curl -X PUT http://localhost:8001/site/{site_id} \
  -H "Content-Type: application/json" \
  -d '{
    "version": "2.0",
    "owner_name": "Jane Doe",
    "owner_email": "jane@example.com",
    "type": "ROOT"
  }'

# Delete a site
curl -X DELETE http://localhost:8001/site/{site_id}
```

-----

## 📊 API Documentation

### Core Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | / | Health check |
| GET | /health | Detailed health status |
| POST | /scan | Create new scan job |
| POST | /scan/immediate | Immediate test scan |
| GET | /sites | List all sites |
| PUT | /site/{site\_id} | Update site details |
| DELETE | /site/{site\_id} | Delete site |
| GET | /status/{job\_id} | Get job status |
| GET | /result/{job\_id} | Get scan results |

**Interactive API Documentation**
Visit `http://localhost:8001/docs` for Swagger UI with interactive API testing.

### Example API Response

*Response Structure:*

```json
{
  "url": "[https://example.com](https://example.com)",
  "scannedAt": "2025-10-24T10:30:00",
  "totalUniqueCookies": 25,
  "summaryByCategory": {
    "Essential": 5,
    "Analytics": 10,
    "Advertising": 8,
    "Functional": 2
  },
  "cookies": [
    {
      "name": "_ga",
      "category": "Analytics",
      "domain": "example.com",
      "purpose": "Google Analytics tracking cookie...",
      "duration_human": "2 years",
      "secure": true,
      "httpOnly": false,
      "sameSite": "Lax",
      "vendor": "Google Analytics",
      "is_third_party": false,
      "confidence": 0.99
    }
  ],
  "scanMetadata": {
    "duration_seconds": 45.2,
    "pages_scanned_count": 15,
    "consent_interactions": 1,
    "pages_scanned_details": [
      {
        "url": "[https://example.com](https://example.com)",
        "status": "COMPLETED",
        "scan_duration_seconds": 3.5,
        "cookies_found": 12
      }
    ]
  },
  "complianceInsights": {
    "total_cookies": 25,
    "third_party_cookies": 8,
    "tracking_cookies": 18,
    "compliance_score": 52,
    "gdpr_impact": "high",
    "ccpa_impact": "high"
  },
  "recommendations": [
    "Implement cookie consent banner for analytics and advertising cookies",
    "Review third-party cookie usage and consider alternatives"
  ]
}
```

-----

## 🐛 Troubleshooting

**Docker Issues**

  * **Services Not Starting**
    ```bash
    # Check service logs
    docker-compose logs backend
    docker-compose logs celery_worker
    docker-compose logs postgresql

    # Restart services
    docker-compose restart backend
    docker-compose restart celery_worker
    ```
  * **Port Already in Use**
    ```bash
    # Find process using port
    lsof -i :8001  # macOS/Linux
    netstat -ano | findstr :8001  # Windows

    # Change port in docker-compose.yml
    services:
      backend:
        ports:
          - "8002:8000"  # Use different port
    ```
  * **Database Connection Issues**
    ```bash
    # Check PostgreSQL is running
    docker-compose exec postgresql pg_isready -U admin

    # Reinitialize database
    docker-compose exec backend python init_db.py
    ```

**Scanner Issues**

  * **Playwright Browser Not Found**
    ```bash
    # Reinstall browsers in Docker
    docker-compose exec backend playwright install chromium

    # For manual setup
    playwright install chromium
    playwright install-deps chromium
    ```
  * **Scanning Timeout**
    Increase timeout in scan options:
    ```json
    {
      "options": {
        "wait_seconds": 10,
        "banner_timeout": 15
      }
    }
    ```

**AI Enrichment Issues**

  * **Invalid API Key**
    ```bash
    # Test your API key
    docker-compose exec backend python list_models.py

    # Update .env with valid key
    GOOGLE_API_KEY="your-valid-key-here"

    # Restart services
    docker-compose restart backend celery_worker
    ```
  * **Rate Limiting**
    The system automatically handles rate limits, but you can:
      * Add delays between scans
      * Use a different API key
      * Upgrade your Google AI Studio quota

**Common Error Messages**
| Error | Solution |
| :--- | :--- |
| Connection refused | Check if all services are running with `docker-compose ps` |
| Database does not exist | Run `docker-compose exec backend python init_db.py` |
| Playwright executable not found | Run `playwright install chromium` |
| API key invalid | Update `GOOGLE_API_KEY` in `.env` |
| Port already in use | Change ports in `docker-compose.yml` |

-----

## 💻 Development

**Running Tests**

```bash
# Backend tests (if available)
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

**Debugging**

  * **Backend Debugging**
    ```bash
    # Enable verbose logging
    export LOG_LEVEL=DEBUG
    uvicorn main:app --reload --log-level debug
    ```
  * **Check Celery Tasks**
    ```bash
    # Monitor Celery worker
    docker-compose logs -f celery_worker

    # Or manually
    celery -A worker.celery_app worker --loglevel=debug
    ```
  * **Database Inspection**
    ```bash
    # Access PostgreSQL shell
    docker-compose exec postgresql psql -U admin -d cookie_consent_db

    # Common queries
    SELECT * FROM sites;
    SELECT * FROM jobs ORDER BY created_at DESC LIMIT 10;
    SELECT * FROM enriched_cookies WHERE job_id = 'your-job-id';
    ```
  * **Redis Inspection**
    ```bash
    # Access Redis CLI
    docker-compose exec redis redis-cli

    # Check queue
    KEYS *
    LLEN celery
    ```

-----

## 🔧 Advanced Configuration

**Increasing Scan Performance**
Edit `docker-compose.yml`:

```yaml
services:
  celery_worker:
    command: celery -A worker.celery_app worker --loglevel=info --concurrency=4
    environment:
      MAX_CONCURRENT_SCANS: 5
```

**Custom Cookie Database**
Place your `exhaustive_cookie_database.json` in `backend_kritesh/`:

```json
{
  "custom_cookie_name": {
    "type": "Analytics",
    "provider": "Custom Provider",
    "duration_human": "1 year",
    "description": "Custom cookie description"
  }
}
```

-----

## 📝 Notes

  * **First scan** may take longer as Playwright downloads browser binaries
  * **AI enrichment** requires a valid Google API key
  * **Concurrent scans** are limited to prevent resource exhaustion
  * **Cookie database** grows automatically as new cookies are discovered
  * **HTTPS sites** are recommended for accurate cookie detection

-----

## 🎉 Quick Start Checklist

  - [ ] Docker and Docker Compose installed
  - [ ] Repository cloned
  - [ ] `.env` file created with Google API key
  - [ ] `docker-compose build` executed
  - [ ] `docker-compose up -d` running
  - [ ] Database initialized with `init_db.py`
  - [ ] Frontend accessible at `http://localhost:3000`
  - [ ] Backend accessible at `http://localhost:8001`
  - [ ] First test scan completed successfully

You're ready to scan\! 🚀

-----

## 🤝 Contributing

We welcome contributions\! Please see our contributing guidelines for details.

### Development Workflow

1.  **Fork** the repository
2.  **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3.  **Commit** your changes (`git commit -m 'Add amazing feature'`)
4.  **Push** to the branch (`git push origin feature/amazing-feature`)
5.  **Open** a Pull Request

### Code Style

  - Follow [ESLint](https://eslint.org/) rules
  - Use [Prettier](https://prettier.io/) for formatting
  - Write meaningful commit messages
  - Add tests for new features

-----

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/AGILAN2005/cookie-scanner/blob/main/LICENSE) file for details.

-----

## 🆘 Support

\<div align="center"\>

**Need help?**
For issues and questions, please:

[](README.md)
[](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/AGILAN2005/cookie-scanner/issues)
[](https://www.google.com/search?q=https://github.com/AGILAN2005/cookie-scanner%23troubleshooting)

\</div\>

-----

## 🙏 Acknowledgments

  - **Open Source Contributors** for the amazing tools
  - **FastAPI** & **React** communities for guidance
  - **Playwright** team for the powerful browser automation

-----

\<div align="center"\>

**⭐ Star this repository if you find it helpful\!**

[](https://www.google.com/search?q=https://github.com/AGILAN2005/cookie-scanner/stargazers)
[](https://www.google.com/search?q=https://github.com/AGILAN2005/cookie-scanner/network)
[](https://www.google.com/search?q=https://github.com/AGILAN2005/cookie-scanner/watchers)

\</div\>

```
```
