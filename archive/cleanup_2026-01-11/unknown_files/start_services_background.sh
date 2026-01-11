#!/bin/bash
# Start all services in background mode (Unix/Mac)
# This script runs main.py with --background flag

echo "Starting services in background..."
python main.py --background

if [ $? -eq 0 ]; then
    echo ""
    echo "Services started successfully!"
    echo "To check status: python main.py --status"
    echo "To stop services: python main.py --stop"
else
    echo ""
    echo "Failed to start services. Check the output above."
    exit 1
fi

