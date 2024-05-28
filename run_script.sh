#!/bin/bash

while true; do
    source $HOME/AI-Picture-Frame/.venv/bin/activate
    python3 $HOME/AI-Picture-Frame/helloworld.py
    deactivate
    sleep 300
done