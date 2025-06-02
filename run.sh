#!/bin/bash

# Quick run script for Document Converter

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Create necessary directories
mkdir -p uploads outputs

# Run the application
echo "🚀 Starting Document Converter & Text Splitter..."
echo "📱 Open http://localhost:5000 in your browser"
echo "⏹️  Press Ctrl+C to stop"
echo ""

python app.py
