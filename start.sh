#!/bin/bash
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Seeding database..."
python seed.py

echo "Starting server..."
uvicorn app.main:app --reload
