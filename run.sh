#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    if ! python3 -m venv venv; then
        echo "Failed to create virtual environment. Please make sure python3-venv is installed:"
        echo "sudo apt-get install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

clear

# Run the application
echo "Starting the application..."
python main.py

# Deactivate virtual environment when done
deactivate 