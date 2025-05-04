#!/bin/bash

# Get the current user's home directory
HOME_DIR=$(eval echo ~$USER)

# Change to the project directory
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Run the program
python main.py --refresh-second 100 > "$HOME_DIR/frame_script_output.log" 2>&1