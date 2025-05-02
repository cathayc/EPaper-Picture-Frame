#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import time
import sys

import signal
import argparse

from helpers.epaper import setup_gpio, cleanup_gpio, exithandler, display_images
from helpers.connection import download_images_from_folder


def main(refresh_second, folder_path):
    print(f"refresh second: {refresh_second}")
    signal.signal(signal.SIGTERM, exithandler)
    signal.signal(signal.SIGINT, exithandler)
    
    setup_gpio()  # Set up the GPIO pins
    imgPath = "Images"
    try:
        download_images_from_folder(imgPath, folder_path)
    except:
        pass
    display_images(imgPath, refresh_second)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Feature flag in Python")
    parser.add_argument("--refresh-second", type=int, default = 15, help="Add the number of seconds you'd like the paper to refresh at. Default to 15.")
    parser.add_argument("--folder-path", type=str, default = "/AI Picture Frame", help="Add the number of seconds you'd like the paper to refresh at. Default to 15.")
    args = parser.parse_args()

    main(args.refresh_second, args.folder_path)