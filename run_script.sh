#!/bin/bash
cd /home/cathychang/AI-Picture-Frame
source .venv/bin/activate
python main.py --refresh-second 100 > /home/cathychang/frame_script_output.log 2>&1