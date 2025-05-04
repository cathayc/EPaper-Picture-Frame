#!/bin/bash
cd /EPpaper-Picture-Frame
source .venv/bin/activate
python main.py --refresh-second 100 > /home/frame_script_output.log 2>&1