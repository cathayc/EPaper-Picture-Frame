#!/bin/bash

# Get the current user and home directory
CURRENT_USER=$(whoami)
HOME_DIR=$(eval echo ~$CURRENT_USER)
PROJECT_DIR="$HOME_DIR/EPaper-Picture-Frame"

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

echo ""
echo "To check service status, run:"
echo "sudo systemctl status epaper-frame"

# Change to the project directory
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Run the program
python main.py --refresh-second 100 > "$HOME_DIR/frame_script_output.log" 2>&1