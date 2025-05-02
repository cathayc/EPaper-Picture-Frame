import os
import io
import requests
import re

from config import GOOGLE_DRIVE_FOLDER_ID

def get_direct_download_link(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def download_images_from_folder(local_destination, folder_path):
    print("Checking to download images from Google Drive")
    
    # Create the directory if it doesn't exist
    try:
        if not os.path.exists(local_destination):
            os.makedirs(local_destination, mode=0o755, exist_ok=True)
    except PermissionError:
        print(f"Warning: Could not create directory {local_destination}. Using current directory instead.")
        local_destination = "."
    
    try:
        # Get the folder page content
        folder_url = f"https://drive.google.com/drive/folders/{GOOGLE_DRIVE_FOLDER_ID}"
        response = requests.get(folder_url)
        
        # Extract file IDs using regex
        file_ids = re.findall(r'data-id="([^"]+)"', response.text)
        if "_gd" in file_ids: file_ids.remove("_gd")
        print(f"Google drive files: {file_ids}")
        gd_file_names = set()

        # Get current files in local destination
        current_files = set(os.listdir(local_destination))
        
        print("Current files:", current_files)
        
        # Process each file
        for file_id in file_ids:
            # Get file info
            file_url = f"https://drive.google.com/file/d/{file_id}/view"
            file_response = requests.get(file_url)
            
            # Extract filename
            filename_match = re.search(r'<title>([^<]+) - Google Drive</title>', file_response.text)
            if not filename_match:
                continue
                
            file_name = filename_match.group(1)
            local_path = os.path.join(local_destination, file_name)
            gd_file_names.add(file_name.split('.')[0])
            
            # Skip if file already exists
            if file_name in current_files:
                continue
                
            print(f"Downloading file: {file_name}")
            
            # Download the file
            download_url = get_direct_download_link(file_id)
            file_response = requests.get(download_url)
            
            # Save the file
            with open(local_path, 'wb') as f:
                f.write(file_response.content)
            print(f"File downloaded successfully as {local_path}")
            
        # Remove files that are no longer in Google Drive
        for local_file in current_files:
            if local_file.split('.')[0] not in gd_file_names:
                try:
                    os.remove(os.path.join(local_destination, local_file))
                    print(f"Deleted file: {local_file}")
                except Exception as e:
                    print(f"Warning: Could not delete file {local_file}: {e}")
                
    except Exception as e:
        print(f"An error occurred: {e}") 