#!/bin/bash

# Exit on errors
set -e

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py