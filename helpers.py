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
            retrieved_path_map = {os.path.join(local_destination, os.path.basename(file['path_display'])): file['path_display'] for file in files}
            retrieved_file_paths = [os.path.join(local_destination, os.path.basename(file['path_display'])) for file in files]
            current_file_paths = [os.path.join(local_destination, file) for file in os.listdir(local_destination)]
            # Files in current file path that's not in retrieved file path:
            files_to_delete = list(set(current_file_paths) - set(retrieved_file_paths))
            files_to_add = list(set(retrieved_file_paths) - set(current_file_paths))

            # Delete files that are not in the retrieved file paths
            for file in files_to_delete:
                os.remove(file)
                print(f"Deleted file: {file}")
            
            # Add files that are not in the current file paths
            for file in files_to_add:
                # Reextract this: os.path.basename(file['path_display']
                dropbox_fp = retrieved_path_map[file]
                print("Downloading file:", dropbox_fp)
                # Create the directory structure if it doesn't exist
                os.makedirs(os.path.dirname(file), exist_ok=True)

                # Dropbox API endpoint for downloading files
                download_url = 'https://content.dropboxapi.com/2/files/download'

                # Specify Dropbox API headers for downloading
                download_headers = {
                    'Authorization': f'Bearer {dropbox_access_token}',
                    'Dropbox-API-Arg': f'{{"path": "{dropbox_fp}"}}'
                }

                # Make a request to download the file
                download_response = requests.post(download_url, headers=download_headers)

                # Save the downloaded file locally
                with open(file, 'wb') as local_file:
                    local_file.write(download_response.content)
                    print("File downloaded successfully as ", file)
        except requests.exceptions.JSONDecodeError:
            # Print the response content if there is an issue with JSON decoding
            print(response.text)
    # Unauthorized response
    elif response.status_code == 401:
        pass
    else:
        # Print the response content for non-OK status codes
        print(response.text)

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

        setup_gpio()

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
            try:
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