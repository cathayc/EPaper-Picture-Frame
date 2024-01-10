import requests
import os

from config import dropbox_access_token

def download_images_from_folder(local_destination):
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
          
