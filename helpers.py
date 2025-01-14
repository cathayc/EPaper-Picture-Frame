import requests
import math
import os
import random
import time
import sys
import RPi.GPIO as GPIO
from PIL import Image
from waveshare_epd import epd7in5_V2 as epd_driver

from config import dropbox_access_token

def download_images_from_folder(local_destination):
    print("Checking to download images from Dropbox")
    # Dropbox API endpoint for listing files in a folder
    list_folder_url = 'https://api.dropboxapi.com/2/files/list_folder'

    # Specify Dropbox API headers, including the access token
    headers = {
        'Authorization': f'Bearer {dropbox_access_token}',
        'Content-Type': 'application/json',
    }

    # Specify the folder path for which you want to list files
    folder_path = '/AI Picture Frame'
    data = {
        'path': folder_path,
        'recursive': False,
    }

    # Make a request to list files in the folder
    response = requests.post(list_folder_url, headers=headers, json=data)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        try:
            # Try to parse the response as JSON
            files = response.json().get('entries', [])

            # Iterate through the files and download each image
            for file_info in files:
                file_path = file_info['path_display']
                local_file_path = os.path.join(local_destination, os.path.basename(file_path))

                # Check if the file already exists locally
                if not os.path.exists(local_file_path):
                    print("Downloading file:", file_path)
                    # Create the directory structure if it doesn't exist
                    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                    # Dropbox API endpoint for downloading files
                    download_url = 'https://content.dropboxapi.com/2/files/download'

                    # Specify Dropbox API headers for downloading
                    download_headers = {
                        'Authorization': f'Bearer {dropbox_access_token}',
                        'Dropbox-API-Arg': f'{{"path": "{file_path}"}}'
                    }

                    # Make a request to download the file
                    download_response = requests.post(download_url, headers=download_headers)

                    # Save the downloaded file locally
                    with open(local_file_path, 'wb') as local_file:
                        local_file.write(download_response.content)
                        print("File downloaded successfully as ", local_file_path)
        except requests.exceptions.JSONDecodeError:
            # Print the response content if there is an issue with JSON decoding
            print(response.text)
    else:
        # Print the response content for non-OK status codes
        print(response.text)

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

def check_and_delete_images(imgPath):
    imagedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), imgPath)
    images = list(filter(supported_filetype, os.listdir(imagedir)))
    # Check if the number of images exceeds 10
    if len(images) > 6:
        # Sort the images by creation time (you may need to implement your own sorting logic)
        images.sort(key=lambda x: os.path.getctime(os.path.join(imagedir, x)))

        # Delete the earliest 5 images and remove them from the directory
        for i in range(len(images)-4):
            # Build the full file path to the image
            image_path = os.path.join(imagedir, images[i])
            # Delete the image file
            os.remove(image_path)

        # Refresh the list of images in t

def display_images(imgPath, refresh_second, loop = True):
    # Ensure this is the correct path to your video folder
    imagedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), imgPath)
    print(imagedir)
    epd = epd_driver.EPD()
    width = epd.width
    height = epd.height

    try:
        print('Initiating')
        epd.init()
        print('Clearing')
        epd.Clear()

        ordered_images = list(filter(supported_filetype, os.listdir(imagedir)))
        images = random.sample(ordered_images, len(ordered_images))
        if not images:
            print("No images found")
            sys.exit()
        
        # Want this to be looping if the loop = True
        count = 0
        while (count < len(images) and not loop) or loop:
            print(count)
            # Mod this
            # single_image = images[count % len(images)]
            len(images)
            random_index = random.randint(0, len(images) - 1)
            single_image = images[random_index]
            # Get current images
            currentImage = os.path.join(imagedir, single_image)
            image = Image.open(currentImage)
            print('Current image name: ', currentImage)
            image = image.resize((width, height))

            bmp_image = image.convert("RGB")
            print('Successfully converted to bmp image')

            print('Displaying')
            epd.display(epd.getbuffer(bmp_image))
            count= count + 1
            time.sleep(refresh_second)
            # Download images from folder if we successfully looped through all images
            if count % len(images) == 0:
                download_images_from_folder(imgPath)
                # Update the images list
                ordered_images = list(filter(supported_filetype, os.listdir(imagedir)))
                images = random.sample(ordered_images, len(ordered_images))
        print('Closing...')
        epd.reset()

    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()  # Clean up the GPIO pins