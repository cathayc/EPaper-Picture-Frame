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
    
    # # First, call leo and save images
    # if call_leo:
    #     # Calling to Leo with user prompt
    #     imgPath = "Images/PromptLeoImages"
    #     prompt = call_leo
    #     call_and_save(prompt, imgPath)
    #     display_images(imgPath, refresh_second)
    #     check_and_delete_images(imgPath)
    # elif random_call_leo:
    #     # Calling to Leo with random prompt
    #     imgPath = "Images/RandomLeoImages"
    #     prompt = choose_random_words()
    #     print(f"Your random words turned out to be: {prompt}")
    #     call_and_save(prompt, imgPath)
    #     display_images(imgPath, refresh_second)
    #     check_and_delete_images(imgPath)
    # else:
        # # Default to general images taken from dropbox
        # imgPath = "Images/GeneralImages"
        # download_images_from_folder(imgPath)
        # display_images(imgPath, refresh_second)
    # At the very end, loop into general images
    print("Playing default now")
    setup_gpio()  # Set up the GPIO pins
    imgPath = "Images/GeneralImages"
    download_images_from_folder(imgPath)
    display_images(imgPath, refresh_second, loop = True)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example of a feature flag in Python")
    parser.add_argument("--call-leo", type=str, help="Call Leonardo AI with the specified prompt")
    parser.add_argument("--random-call-leo", action="store_true", help="Call Leonardo AI with randomly generated words")
    parser.add_argument("--refresh-second", type=int, default = 15, help="Add the number of seconds you'd like the paper to refresh at")
    args = parser.parse_args()

    main(args.call_leo, args.random_call_leo, args.refresh_second)