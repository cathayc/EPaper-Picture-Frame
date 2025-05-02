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

def supported_filetype(file):
    _, ext = os.path.splitext(file)
    return ext.lower() in(".png", ".jpg")

def display_images(imgPath, refresh_second, loop = True):
    # Ensure this is the correct path to your video folder
    imagedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), imgPath)
    
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

        ordered_images = list(filter(supported_filetype, os.listdir(imagedir)))
        images = random.sample(ordered_images, len(ordered_images))
        if not images:
            print("No images found")
            sys.exit()
        
        # Want this to be looping if the loop = True
        count = 0
        while loop:
            print(count)
            # Mod this
            # single_image = images[count % len(images)]
            random_index = random.randint(0, len(images) - 1)
            single_image = images[random_index]
            # Get current images
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
            # Download images from folder if we successfully looped through all images
            if count % len(images) == 0:
                try:
                    download_images_from_folder(imgPath)
                except:
                    pass
                # Update the images list
                new_ordered_images = list(filter(supported_filetype, os.listdir(imagedir)))
                if ordered_images != new_ordered_images:
                    print(f"Images updated to: {new_ordered_images}")
                    # TODO: Delete old images
                ordered_images = new_ordered_images
                images = random.sample(ordered_images, len(ordered_images))
        print('Closing...')
        epd.reset()

    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()  # Clean up the GPIO pins