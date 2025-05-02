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

def is_image_file(file_path):
    """Check if file is an image by trying to open it with PIL"""
    try:
        with Image.open(file_path) as img:
            # Try to load the image to verify it's valid
            img.load()
            return True
    except Exception as e:
        print(f"Not a valid image file {file_path}: {e}")
        return False

def convert_to_jpg(image_path):
    """Convert any image format to JPG"""
    try:
        # Open image file
        with Image.open(image_path) as image:
            # Create JPG path by replacing extension
            jpg_path = os.path.splitext(image_path)[0] + '.jpg'
            
            # Convert and save as JPG
            image.convert('RGB').save(jpg_path, 'JPEG', quality=95)
            
            # Verify the new file exists and is valid
            if not is_image_file(jpg_path):
                print(f"Conversion failed: {jpg_path} is not a valid image")
                if os.path.exists(jpg_path):
                    os.remove(jpg_path)            
            
            # Remove original file if it's not already a jpg
            if not image_path.lower().endswith('.jpg'):
                os.remove(image_path)
            
            print(f"Successfully converted {image_path} to {jpg_path}")
    except Exception as e:
        print(f"Failed to convert file {image_path}: {e}")
        # Clean up any partial conversion
        jpg_path = os.path.splitext(image_path)[0] + '.jpg'
        if os.path.exists(jpg_path):
            os.remove(jpg_path)

def process_image_file(file_path):
    """Process image file, converting to JPG if needed"""
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        
    if not is_image_file(file_path):
        print(f"Skipping non-image file: {file_path}")
        
    if not file_path.lower().endswith('.jpg'):
        print(f"Converting non-JPG image: {file_path}")
        convert_to_jpg(file_path)

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

def convert_files_to_jpg(imgPath):
    for file in os.listdir(imgPath):
        file_path = os.path.join(imgPath, file)
        process_image_file(file_path)

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

        # First convert all files to JPG, then process the images
        print(f"Processing images in {imagedir}")
        convert_files_to_jpg(imagedir)
        
        ordered_images = []
        for file in os.listdir(imagedir):
            file_path = os.path.join(imagedir, file)
            ordered_images.append(os.path.basename(file_path))

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
            # Download images from folder if we successfully looped through all images
            if count % len(images) == 0:
                try:
                    download_images_from_folder(imgPath)
                except:
                    pass
                # Update the images list
                new_ordered_images = []
                for file in os.listdir(imagedir):
                    file_path = os.path.join(imagedir, file)
                    processed_path = process_image_file(file_path)
                    if processed_path:
                        new_ordered_images.append(os.path.basename(processed_path))
                
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