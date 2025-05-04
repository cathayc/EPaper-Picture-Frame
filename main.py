#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import time
import sys

import signal
import argparse

from helpers.epaper import setup_gpio, cleanup_gpio, exithandler, display_images


def main(refresh_second):
    signal.signal(signal.SIGTERM, exithandler)
    signal.signal(signal.SIGINT, exithandler)
    print(f"refresh second: {refresh_second}")
    
    setup_gpio()  # Set up the GPIO pins
    display_images(refresh_second)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Feature flag in Python")
    parser.add_argument("--refresh-second", type=int, default = 15, help="Add the number of seconds you'd like the paper to refresh at. Default to 15.")
    args = parser.parse_args()

    main(args.refresh_second)