#!/bin/bash

# Exit on error
set -e

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libheif-dev

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! To activate the virtual environment, run:"
echo "source .venv/bin/activate"

chmod +x setup.sh && ./setup.sh