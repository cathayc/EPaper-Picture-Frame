from helpers.connection import download_images_from_folder, clean_up_image_files
from config import GOOGLE_DRIVE_FOLDER_ID

download_images_from_folder("/Users/cathychang/Desktop/Projects/Epaper-Picture-Frame/Images", GOOGLE_DRIVE_FOLDER_ID)
clean_up_image_files("/Users/cathychang/Desktop/Projects/Epaper-Picture-Frame/Images")