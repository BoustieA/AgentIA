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
COPY Requirements/requirements_UI.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_UI.txt

# Copy the rest of the app
COPY UI/ .

# Expose Streamlit default port
#EXPOSE 8501

# Run the application
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]