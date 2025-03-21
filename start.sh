#!/bin/bash

# Exit on error
set -e

echo "Starting backend (FastAPI)..."
cd backend
uvicorn main:app --reload &
BACKEND_PID=$!
cd ..

echo "Starting frontend (React)..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Trap Ctrl+C to stop both
trap "echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID" INT

# Wait for both processes to end
wait $BACKEND_PID $FRONTEND_PID
