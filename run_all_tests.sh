#!/bin/bash

set -e

# Check for Python 3
if ! command -v python3 &> /dev/null; then
  echo "Python 3 is required but not found. Exiting."
  exit 1
fi

# Create venv if not exists
if [ ! -d "automation/venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv automation/venv
fi

# Activate venv
source automation/venv/bin/activate

# Install dependencies if needed
if [ ! -f "automation/venv/.deps_installed" ] || [ automation/requirements.txt -nt automation/venv/.deps_installed ]; then
  echo "Installing Python dependencies..."
  pip install --upgrade pip
  pip install -r automation/requirements.txt
  touch automation/venv/.deps_installed
fi

# Install locust if not present (for performance tests)
if ! pip show locust &> /dev/null; then
  echo "Installing locust..."
  pip install locust
fi

# Find and kill any process using port 8000 (uvicorn default)
PORT=8000
PID=$(lsof -ti tcp:$PORT || true)
if [ -n "$PID" ]; then
  echo "Killing process on port $PORT (PID: $PID)"
  kill -9 $PID
  sleep 1
fi

# Start FastAPI server in background
cd automation
source venv/bin/activate
uvicorn server.backend:app --port $PORT --reload &
SERVER_PID=$!
cd ..

# Wait for server to start
sleep 2

# Run all tests
pytest automation/tests
TEST_RESULT=$?

# Stop the server
echo "Stopping server (PID: $SERVER_PID)"
kill -9 $SERVER_PID

exit $TEST_RESULT 