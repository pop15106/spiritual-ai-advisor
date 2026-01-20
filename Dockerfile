# Use specific python version that matches user environment closest or stable
FROM python:3.10-slim

# Install system dependencies
# libsqlite3-dev is required for building some python packages that Kerykeion depends on
# gcc and build-essential are often needed for compiling
RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    libsqlite3-0 \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
# Using the command from Procfile: gunicorn api:app --bind 0.0.0.0:$PORT
# Note: Railway sets $PORT environment variable automatically
CMD gunicorn api:app --bind 0.0.0.0:$PORT
