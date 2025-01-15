# Introduction

This project is born out of curiousity on how ePaper displays work. It is a picture frame that can do the following two tasks:
1. Slowly display pre-uploaded image on the ePaper display
2. Take in a user-inputted prompt, generate + download AI images, and display images on the ePaper display

## Table Of Contents

- [Install](#install)
- [Usage](#usage)
  - [Normal Usage](#normal-usage)
  - [Prompted AI Images](#prompted-ai-images)

## Install

**Note:** Some of these installation instructions takes from Tom Whitell's [SlowMovie](https://github.com/TomWhitwell/SlowMovie) setup instructions. This installation instruction assumes you have access to your Raspberry Pi and that you have the hardware set up properly. See the [Medium post](https://debugger.medium.com/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4) for more complete instructions. AI Picture Frame requires [Python 3](https://www.python.org). It uses [FFmpeg](https://ffmpeg.org) via [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) for video processing, [Pillow](https://python-pillow.org) for image processing, and [Omni-EPD](https://github.com/robweber/omni-epd) for loading the correct e-ink display driver. [ConfigArgParse](https://github.com/bw2/ConfigArgParse) is used for configuration and argument handling.

On the Raspberry Pi (or after ssh-ing into the Raspberry Pi):
0. Make sure SPI is enabled
   * Run `sudo raspi-config`
   * Navigate to `Interface Options` > `SPI`
   * Select `Yes` to enable SPI.
   * Select `<Finish>` to exit. Reboot if prompted.
1. Set up environment
   * Update package sources: `sudo apt update`
   * Make sure git is installed: `sudo apt install git`
   * Make sure pip is installed: `sudo apt install python3-pip`
2. Clone this repo
   * Create a new SSH key and add to your github [Instructions](https://phoenixnap.com/kb/git-clone-ssh)
   * `git clone git@github.com:cathayc/EPaper-Picture-Frame.git`
   * Navigate to the new the project directory: `cd EPaper-Picture-Frame/`
4. Create a virtual environment and make sure requirements are installed
   * `python3 -m venv .venv`
   * `source .venv/bin/activate`
   * `pip3 install git+https://github.com/robweber/omni-epd.git#egg=omni-epd`
   * `pip3 install -r requirements.txt`
5. Test it out
   * Run `python3 main.py`. If everything's installed properly, this should start playing all the pictures from the `Images/GeneralImages` directory.
   * If you'd like to change the refresh cadence, you can use the argument `--refresh-second`. The default is 15 seconds. Example call for refreshing images every 10 seconds: `python3 main.py --refresh-second 10`.

## Usage
There are two types of usages:
1. Slowly display pre-uploaded images
2. Given a prompt, generate AI images and slowly display them

### Normal Usage

The normal usage takes images from `Images/GeneralImages` and slowly displays them. Take the following steps:
1. Run `python3 main.py`. If everything's installed properly, this should start playing all the pictures from the `Images/GeneralImages` directory.
2. If you'd like to change the refresh cadence, you can use the argument `--refresh-second`. The default is 15 seconds. Example call for refreshing images every 10 seconds: `python3 main.py --refresh-second 10`.

### Prompted AI Images
0. To generate AI images, you will need to create a leonardo.ai account. After doing so, you will obtain your own API key. Store this in the config file:
1. Navigate to config.py file at root, and replace `"YOUR-API-KEY"` with your own API key.
2. Call leonardo:
   * Think of a prompt. Example: `cat chase horse in wild west`
   * Add prompt to your call: `python3 main.py --call-leo "cat chase horse in wild west"`
   * The program will now call leonardo with your prompt, download the images, and display on your epaper display.

## Making this script run at startup

To make the script run at startup, you'll need to use the `run_script.sh` and `run_script.service` files found at the root of the directory.

1. At your home directory, add a cron job.
   * Open up the crontab file: `contab -e`
   * Add the line `@reboot /home/cathychang/run_script.sh > /home/cathychang/frame_script_output.log 2>&1`
   * Save and exit (ctrl x + ctrl o)
2. Permissions:
   * Ensure that both the run_script.sh script and the main.py script have the execute permission:
   * `chmod +x /path-to-EPaper-Picture-Frame/run_script.sh`
3. Reload systemd and start the service. Every time you make changes to the service, you'll need to restart it by running the same command:
   * `sudo systemctl status run_script.service`
   * `journalctl -xe`



