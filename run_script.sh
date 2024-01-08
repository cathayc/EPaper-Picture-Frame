#!/bin/bash

while true; do
    source /home/cathychang/AI-Picture-Frame/.venv/bin/activate
    python3 /home/cathychang/AI-Picture-Frame/helloworld.py
    deactivate
    sleep 300
done