import gdown
import os
from config import gdrive_folder_id

def download_images_from_folder(folder_id, output_directory):
    # List files in the folder using the folder ID
    file_list_url = f'https://drive.google.com/drive/folders/{folder_id}'
    file_list = gdown.download(file_list_url, quiet=False)
    print(file_list)

    # Read the file list and download images
    with open(file_list, 'r') as file:
        for line in file:
            # Skip empty lines or comments
            if not line.strip() or line.startswith('#'):
                continue

            # Download each image file
            image_link = line.strip()
            download_image(image_link, output_directory)

    # Clean up: remove the temporary file list
    os.remove(file_list)

def download_image(image_link, output_directory):
    # Extract the file ID from the image link
    file_id = image_link.split('/')[-1]

    # Download the image using gdown
    download_url = f'https://drive.google.com/uc?id={file_id}'
    output_path = os.path.join(output_directory, f'{file_id}.jpg')
    gdown.download(download_url, output_path, quiet=False)