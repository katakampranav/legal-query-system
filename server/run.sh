#!/bin/bash
# Run script for development mode

export PYTHONUNBUFFERED=1

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies using uv
echo "Installing dependencies with uv..."
uv sync

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the application
echo "Starting Legal QA Server..."
uv run uvicorn src.app.api:app --reload --host 0.0.0.0 --port 8002
