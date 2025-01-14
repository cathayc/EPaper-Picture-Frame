#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import time
import sys

import signal
import argparse

from leonardo import call_and_save as call_and_save
from helpers import setup_gpio, cleanup_gpio, exithandler, display_images, download_images_from_folder


def main(call_leo, random_call_leo, refresh_second):
    print(f"refresh second: {refresh_second}")
    signal.signal(signal.SIGTERM, exithandler)
    signal.signal(signal.SIGINT, exithandler)
    
    setup_gpio()  # Set up the GPIO pins
    imgPath = "Images/GeneralImages"
    try:
        download_images_from_folder(imgPath)
    except:
        pass
    display_images(imgPath, refresh_second)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example of a feature flag in Python")
    parser.add_argument("--call-leo", type=str, help="Call Leonardo AI with the specified prompt")
    parser.add_argument("--random-call-leo", action="store_true", help="Call Leonardo AI with randomly generated words")
    parser.add_argument("--refresh-second", type=int, default = 15, help="Add the number of seconds you'd like the paper to refresh at")
    args = parser.parse_args()

    main(args.call_leo, args.random_call_leo, args.refresh_second)