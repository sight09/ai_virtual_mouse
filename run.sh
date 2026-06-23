#!/bin/bash

# AI Virtual Mouse - Unix Launcher
# This script sets up and runs the Virtual Mouse application

echo ""
echo "================================"
echo "  AI Virtual Mouse - Launcher"
echo "================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if ! python3 -m pip show mediapipe > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "================================"
echo "  Starting AI Virtual Mouse"
echo "================================"
echo ""

# Run the application
python3 main.py

# Check for errors
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Application exited with error"
    read -p "Press Enter to exit..."
fi
