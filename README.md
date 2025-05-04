# E-Paper Picture Frame

This project creates a digital picture frame using a Raspberry Pi and an e-Paper display. It downloads images from a Google Drive folder and displays them on the e-Paper screen.

## Features

- Downloads images from Google Drive
- Supports various image formats including HEIC
- Automatic image conversion to compatible formats
- Configurable refresh rate
- Runs headless on Raspberry Pi

## Hardware Requirements

- Raspberry Pi (tested on Raspberry Pi OS)
- SD card (for the Raspberry Pi)
- Waveshare 7.5" e-Paper display (or compatible)

## Table Of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running at Startup](#running-at-startup)

## Installation

1. Enable SPI on your Raspberry Pi:
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > SPI
   # Select Yes to enable SPI
   # Select Finish to exit
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/EPaper-Picture-Frame.git
   cd EPaper-Picture-Frame
   ```

3. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

The setup script will:
- Install required system dependencies
- Create a Python virtual environment
- Install Python packages
- Set up the necessary configurations

## Configuration

1. Create a `config.py` file in the root directory:
   ```python
   GOOGLE_DRIVE_FOLDER_ID = "your_folder_id_here"
   ```

2. Get your Google Drive folder ID:
   - Open your Google Drive folder in a web browser
   - The folder ID is in the URL: `https://drive.google.com/drive/folders/FOLDER_ID`

## Usage

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Run the program:
   ```bash
   python main.py
   ```

3. Optional: Change the refresh rate (default is 15 seconds):
   ```bash
   python main.py --refresh-second 10
   ```

## Running at Startup

1. Create a systemd service:
   ```bash
   sudo nano /etc/systemd/system/epaper-frame.service
   ```

2. Add the following content:
   ```ini
   [Unit]
   Description=E-Paper Picture Frame
   After=network.target

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/EPaper-Picture-Frame
   ExecStart=/home/pi/EPaper-Picture-Frame/.venv/bin/python main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl enable epaper-frame
   sudo systemctl start epaper-frame
   ```

4. Check the status:
   ```bash
   sudo systemctl status epaper-frame
   ```

## Troubleshooting

- If images aren't displaying, check the permissions of the `Images` directory
- For HEIC conversion issues, ensure `libheif-dev` and `libheif-examples` are installed
- Check the systemd service logs: `journalctl -u epaper-frame`