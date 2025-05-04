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

echo "Setting up systemd service..."
# Create service file
sudo tee /etc/systemd/system/epaper-frame.service > /dev/null << EOL
[Unit]
Description=E-Paper Picture Frame
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/run_script.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Make run_script.sh executable
chmod +x run_script.sh

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable epaper-frame
sudo systemctl start epaper-frame

echo "Setup complete! To activate the virtual environment, run:"
echo "source .venv/bin/activate"
echo ""
echo "To check service status, run:"
echo "sudo systemctl status epaper-frame"

chmod +x setup.sh && ./setup.sh