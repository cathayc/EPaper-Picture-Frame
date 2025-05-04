import requests
import math
import os
import random
import time
import sys
import RPi.GPIO as GPIO
from PIL import Image
import io
from waveshare_epd import epd7in5_V2 as epd_driver
import mimetypes

from helpers.connection import download_images_from_folder

from config import GOOGLE_DRIVE_FOLDER_ID

# Define the setup_gpio function
def setup_gpio():
    # Set up the GPIO pin as an output
    GPIO.setwarnings(False)  # Disable warnings
    GPIO.setmode(GPIO.BCM)  # Set BCM mode
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

def _get_ordered_image_list(imgPath):
    imagedir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), imgPath)
    ordered_images = []
    for file in os.listdir(imagedir):
        file_path = os.path.join(imagedir, file)
        ordered_images.append(os.path.basename(file_path))
    return ordered_images

def display_images(imgPath, refresh_second, loop = True):
    # Ensure this is the correct path to your video folder
    imagedir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), imgPath)
    
    # Set GPIO mode before initializing display
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    epd = epd_driver.EPD()
    width = epd.width
    height = epd.height

    try:
        print('Initiating')
        epd.init()
        print('Clearing')
        epd.Clear()
        setup_gpio()

        download_images_from_folder(imgPath)
        
        ordered_images = _get_ordered_image_list(imgPath)

        images = random.sample(ordered_images, len(ordered_images))
        if not images:
            print("No images found")
            sys.exit()
        
        print(f"Have {len(images)} images to display")
        
        # Want this to be looping if the loop = True
        count = 0
        while loop:
            print(f"Displaying image {count + 1}")
            random_index = random.randint(0, len(images) - 1)
            single_image = images[random_index]
            currentImage = os.path.join(imagedir, single_image)
            try:
                image = Image.open(currentImage)
                print('Current image name: ', currentImage)
                image = image.resize((width, height))

                bmp_image = image.convert("RGB")
                print('Successfully converted to bmp image')

                print('Displaying')
                epd.display(epd.getbuffer(bmp_image))
            except IOError as e:
                print('Display failed')
                print(e)
            count= count + 1
            time.sleep(refresh_second)
            
            # Redownload images every 5 loops
            if count // len(images) == 5:
                download_images_from_folder(imgPath)
                ordered_images = _get_ordered_image_list(imgPath)
                images = random.sample(ordered_images, len(ordered_images))
        print('Closing...')
        epd.reset()

    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()  # Clean up the GPIO pins