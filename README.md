# Introduction

This project is born out of curiousity into how ePaper displays and AI picture generations work. It is a picture frame that can do the following two tasks:
1. Slowly display pre-uploaded image on the ePaper display
2. Take in a user-inputted prompt, generate + download AI images, and display images on the ePaper display

Majority of the ePaper configuration and driver code is derived from [Tom Whitwell's SlowMovie project](https://github.com/TomWhitwell/SlowMovie), whose purpose is to take in a movie and play it slowly, frame by frame, on an ePaper display, using a Raspberry Pi.

## Table Of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
  - [E-ink Display Customization](#e-ink-display-customization)
  - [Running as a Service](#running-as-a-service)

## Background

In December 2018, Bryan Boyer posted [“Creating a Very Slow Movie Player”](https://medium.com/s/story/very-slow-movie-player-499f76c48b62), an essay about light and Brasília and architecture in which Boyer builds an e-paper display that shows films at 24 frames per hour, rather than 24 frames per second so it takes about a year to play the 142 minutes of _2001: A Space Odyssey_.

In August 2020, Tom Whitwell posted ["How to Build a Very Slow Movie Player for £120 in 2020"](https://debugger.medium.com/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4), with instructions on how to build a VSMP with the new [7.5-inch, Raspberry Pi-compatible e-paper display from Waveshare](https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-hat.htm).

In June 2023, Cathy cloned the code and made some modifications to make it work with her (this) project.

SlowMovie is the code that runs a VSMP on a Raspberry Pi.

## Install

**Note:** These installation instructions assume you have access to your Raspberry Pi and that you have the hardware set up properly. See the [Medium post](https://debugger.medium.com/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4) for more complete instructions.

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
2. Install Waveshare e-paper drivers
   * `pip3 install "git+https://github.com/waveshare/e-Paper.git#subdirectory=RaspberryPi_JetsonNano/python&egg=waveshare-epd"`
3. Clone this repo
   * `git clone https://github.com/TomWhitwell/SlowMovie`
   * Navigate to the new SlowMovie directory: `cd SlowMovie/`
   * Copy the default configuration file: `cp Install/slowmovie-default.conf slowmovie.conf`
4. Make sure dependencies are installed
   * `sudo apt install ffmpeg`
   * `pip3 install ffmpeg-python`
   * `pip3 install pillow`
   * `pip3 install ConfigArgParse`
   * `pip3 install git+https://github.com/robweber/omni-epd.git#egg=omni-epd`
5. Test it out
   * Run `python3 slowmovie.py`. If everything's installed properly, this should start playing `test.mp4` (a clip from _Psycho_) from the `Videos` directory.

### E-ink Display Customization

The guide for this program uses the [7.5-inch Waveshare display](https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-hat.htm), this is the device driver loaded by default in the `slowmovie.conf` file. It is possible to specify other devices by editing the file or using the command line `-e` option. You can view a list of compatible e-ink devices on the [Omni-EPD repo](https://github.com/robweber/omni-epd/blob/main/README.md#displays-implemented).

Customizing other options of the display is also possible by creating a file called `omni-epd.ini` in the SlowMovie directory. Common options for this file are listed below with a full explanation of all options available.

```
[Display]
rotate=0  # rotate final image written to display by X degrees [0-360]
flip_horizontal=False  # flip image horizontally
flip_vertical=False  # flip image vertically

[Image Enhancements]
contrast=1  # adjust image contrast, 1 = no adjustment
brightness=1  # adjust image brightness, 1 = no adjustment
sharpness=1  # adjust image sharpness, 1 = no adjustment
```
]
