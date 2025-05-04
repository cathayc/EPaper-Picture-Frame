#!/bin/bash

# Exit on error
set -e

# Get the current user and home directory
CURRENT_USER=$(whoami)
HOME_DIR=$(eval echo ~$CURRENT_USER)
PROJECT_DIR="$HOME_DIR/EPaper-Picture-Frame"

echo "Installing system dependencies..."
# For macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install libheif
# For Linux/Raspberry Pi
else
    sudo apt-get update
    sudo apt-get install -y \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libheif-dev \
        libheif-examples \
        libde265-dev
fi

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Activate virtual environment
echo "Setup complete! Activating the virtual environment (source .venv/bin/activate)"
source .venv/bin/activate