# Introduction

This project is born out of curiousity into how ePaper displays and AI picture generations work. It is a picture frame that can do the following two tasks:
1. Slowly display pre-uploaded image on the ePaper display
2. Take in a user-inputted prompt, generate + download AI images, and display images on the ePaper display

## Table Of Contents

- [Install](#install)
- [Usage](#usage)
  - [E-ink Display Customization](#e-ink-display-customization)
  - [Running as a Service](#running-as-a-service)

## Install

**Note:** Some of these installation instructions takes from Tom Whitell's [SlowMovie](https://github.com/TomWhitwell/SlowMovie) setup instructions. These installation instructions assume you have access to your Raspberry Pi and that you have the hardware set up properly. See the [Medium post](https://debugger.medium.com/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4) for more complete instructions.

SlowMovie requires [Python 3](https://www.python.org). It uses [FFmpeg](https://ffmpeg.org) via [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) for video processing, [Pillow](https://python-pillow.org) for image processing, and [Omni-EPD](https://github.com/robweber/omni-epd) for loading the correct e-ink display driver. [ConfigArgParse](https://github.com/bw2/ConfigArgParse) is used for configuration and argument handling.

_Note that the `omni-epd` package installs Waveshare and Inky EPD driver libraries._
On the Raspberry Pi:

0. Make sure SPI is enabled
   * Run `sudo raspi-config`
   * Navigate to `Interface Options` > `SPI`
   * Select `<Finish>` to exit. Reboot if prompted.
1. Set up environment
   * Update package sources: `sudo apt update`
   * Make sure git is installed: `sudo apt install git`
   * Make sure pip is installed: `sudo apt install python3-pip`
2. Clone this repo
   * `git clone https://github.com/cathayc/AI-Picture-Frame`
   * Navigate to the new the project directory: `cd AI-Picture-Frame/`
4. Create a virtual environment and make sure requirements are installed
   * `python3 -m venv .venv`
   * `source venv/bin/activate`
   * `pip3 install requirements.txt`
5. Test it out
   * Run `python3 helloworld.py`. If everything's installed properly, this should start playing all the pictures from the `Images/OurLoveImages` directory.

### Making this script run at startup

To make the script run at startup, you'll need to use the `run_script.sh` and `run_script.service` files found at the root of the directory.

1. Make sure the paths point to where the files are.
   * In this case, you will want to replace `/home/cathychang/AI-Picture-Frame` in both `run_script.sh` and `run_script.service` to your project directory.
2. Permissions:
   * Ensure that both the run_script.sh script and the helloworld.py script have the execute permission:
   * `chmod +x /path-to-AI-Picture-Frame/run_script.sh`
   * `chmod +x /path-to-AI-Picture-Frame/helloworld.py`
3. Reload systemd and start the service:
   * `sudo systemctl daemon-reload`
   * `sudo systemctl start run_script.service`
4. Check service status, and use the following commands to debug if necessary:
   * `sudo systemctl status run_script.service`




