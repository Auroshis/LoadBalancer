#!/bin/bash

# Optional: wait for etcd to be up (basic sleep or health check)
echo "Waiting for etcd to be ready..."
sleep 3

# Run etcd init script
echo "Initializing etcd config..."
python init_config.py

# Start the FastAPI app
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8080
