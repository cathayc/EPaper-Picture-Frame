#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import time
import sys
import random
import signal
import ffmpeg
import argparse
import RPi.GPIO as GPIO
from PIL import Image
from fractions import Fraction
from leonardo import call_and_save as call_and_save
from waveshare_epd import epd7in5_V2 as epd_driver
import random

def choose_random_words(num_words=5):
    # Open and read the file containing the list of words
    with open("word_list.txt", "r") as file:
        words = file.read().splitlines()

    # Choose 5 random words from the list
    random_words = random.sample(words, num_words)
    random_sentence = " ".join(random_words)
    return random_sentence

# Define the setup_gpio function
def setup_gpio():
    # Set up the GPIO pin as an output
    GPIO.setmode(GPIO.BCM)
    your_pin_number = 20  # Replace with your actual GPIO pin number
    GPIO.setup(your_pin_number, GPIO.OUT)

# Define the cleanup_gpio function
def cleanup_gpio():
    # Clean up GPIO resources
    GPIO.cleanup()

def exithandler(signum, frame):
    try:
        epd_driver.epdconfig.module_exit()
    finally:
        sys.exit()

def supported_filetype(file):
    _, ext = os.path.splitext(file)
    return ext.lower() in(".png", ".jpg")

def main(call_leo, random_call_leo, refresh_second):
    print(f"refresh second: {refresh_second}")
    signal.signal(signal.SIGTERM, exithandler)
    signal.signal(signal.SIGINT, exithandler)
    setup_gpio()  # Set up the GPIO pins
    
    # First, call leo and save images
    if call_leo:
        # Calling to Leo with user prompt
        imgPath = "Images/PromptLeoImages"
        prompt = call_leo
        call_and_save(prompt, imgPath)
        display_images(imgPath, refresh_second)
    elif random_call_leo:
        # Calling to Leo with random prompt
        imgPath = "Images/RandomLeoImages"
        prompt = choose_random_words()
        print(f"Your random words turned out to be: {prompt}")
        call_and_save(prompt, imgPath)
        display_images(imgPath, refresh_second)
    else:
        # Default to love images
        imgPath = "Images/OurLoveImages"
        display_images(imgPath, refresh_second)
    imgPath = "Images/OurLoveImages"
    display_images(imgPath, refresh_second, loop = True)
    
    
def display_images(imgPath, refresh_second, loop = False):
    # Ensure this is the correct path to your video folder
    imagedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), imgPath)
    print(imagedir)
    epd = epd_driver.EPD()
    width = epd.width
    height = epd.height

    try:
        while 1:
            print('Initiating')
            epd.init()
            print('Clearing')
            epd.Clear()

            # Pick a random .mp4 video in your video directory
            images = list(filter(supported_filetype, os.listdir(imagedir)))
            shuffled_list = random.sample(images, len(images))
            print(shuffled_list)
            if not images:
                print("No images found")
                sys.exit()
            
            # Want this to be looping if the loop = True
            count = 0
            while count < len(images) or loop == True:
                # Mod this
                single_image = images[count % len(images)]
                # Get current images
                currentImage = os.path.join(imagedir, single_image)
                image = Image.open(currentImage)
                print('Current image name: ', currentImage)
                image = image.resize((width, height))

                bmp_image = image.convert("RGB")
                print('Successfully converted to bmp image')

                print('Displaying')
                epd.display(epd.getbuffer(bmp_image))
                count+=1
                time.sleep(refresh_second)
            
            print('Closing...')
            epd.reset()

    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()  # Clean up the GPIO pins

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example of a feature flag in Python")
    parser.add_argument("--call-leo", type=str, help="Call Leonardo AI with the specified prompt")
    parser.add_argument("--random-call-leo", action="store_true", help="Call Leonardo AI with random generated tai and cathy words")
    parser.add_argument("--refresh-second", type=int, default = 15, help="Add the number of seconds you'd like the paper to refresh at")
    args = parser.parse_args()

    main(args.call_leo, args.random_call_leo, args.refresh_second)