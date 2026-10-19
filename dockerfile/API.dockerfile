# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for efficient caching
COPY Requirements/requirements_API.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_API.txt

# Copy the rest of the app
COPY DataCollection/ORM_models.py .
COPY API/main.py .