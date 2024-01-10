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
                    # Dropbox API endpoint for downloading files
                    download_url = 'https://content.dropboxapi.com/2/files/download'

                    # Specify Dropbox API headers for downloading
                    download_headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Dropbox-API-Arg': f'{{"path": "{file_path}"}}'
                    }

                    # Make a request to download the file
                    download_response = requests.post(download_url, headers=download_headers)

                    # Save the downloaded file locally
                    with open(local_file_path, 'wb') as local_file:
                        local_file.write(download_response.content)
        except requests.exceptions.JSONDecodeError:
            # Print the response content if there is an issue with JSON decoding
            print(response.text)
    else:
        # Print the response content for non-OK status codes
        print(response.text)
