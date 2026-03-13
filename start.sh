#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Seeding database..."
python seed.py

echo "Starting server..."
uvicorn app.main:app --reload
