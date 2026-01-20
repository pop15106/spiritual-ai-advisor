#!/bin/sh
# Fail on error
set -e

# Support $PORT variable with default of 5000
# This handles the case where PORT might be empty or not set
PORT="${PORT:-5000}"

echo "Starting Spiritual AI Advisor on port $PORT..."

# Run gunicorn with the resolved port
# We use exec to replace the shell process with gunicorn
exec gunicorn api:app --bind "0.0.0.0:$PORT"
