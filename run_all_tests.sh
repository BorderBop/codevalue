#!/bin/bash

set -e

# Find and kill any process using port 8000 (uvicorn default)
PORT=8000
PID=$(lsof -ti tcp:$PORT || true)
if [ -n "$PID" ]; then
  echo "Killing process on port $PORT (PID: $PID)"
  kill -9 $PID
  sleep 1
fi

# Start FastAPI server in background
cd backend
source venv/bin/activate
uvicorn server.backend:app --port $PORT --reload &
SERVER_PID=$!
cd ..

# Wait for server to start
sleep 2

# Run all tests
pytest
TEST_RESULT=$?

# Stop the server
echo "Stopping server (PID: $SERVER_PID)"
kill -9 $SERVER_PID

exit $TEST_RESULT 