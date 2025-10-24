# Enhanced Dockerfile for Backend - World-Class Cookie Scanner

FROM python:3.11-slim

# Set environment variables for consistency
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build tools
    gcc \
    g++ \
    make \
    # PostgreSQL client
    postgresql-client \
    # Network tools
    curl \
    wget \
    # Timezone data
    tzdata \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Use the official Playwright image which includes Python 3.11 and all dependencies
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Install Playwright dependencies first (for better Docker layer caching)
# RUN pip install --no-cache-dir playwright==1.40.0

# # Install Playwright browsers with fixed version for consistency
# RUN playwright install chromium
# RUN playwright install-deps chromium

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application with optimal settings for Docker
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--loop", "asyncio"]