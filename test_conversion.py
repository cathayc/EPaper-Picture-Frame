import os
from helpers.epaper import is_image_file, convert_to_jpg, process_image_file

def test_image_conversion():
    # Test directory
    test_dir = "test_images"
    os.makedirs(test_dir, exist_ok=True)
    
    # Test cases
    test_files = [
        "test.jpg",  # Already JPG
        "test.png",  # PNG to JPG
        "test.heic", # HEIC to JPG
        "test.txt"   # Non-image file
    ]
    
    print("Testing image conversion...")
    
    # Create test files
    for file in test_files:
        file_path = os.path.join(test_dir, file)
        with open(file_path, 'w') as f:
            f.write("test content")
    
    # Test each file
    for file in test_files:
        file_path = os.path.join(test_dir, file)
        print(f"\nTesting {file}:")
        
        # Test is_image_file
        is_image = is_image_file(file_path)
        print(f"is_image_file: {is_image}")
        
        # Test process_image_file
        processed_path = process_image_file(file_path)
        print(f"process_image_file result: {processed_path}")
        
        if processed_path:
            print(f"File exists: {os.path.exists(processed_path)}")
            if os.path.exists(processed_path):
                print(f"File size: {os.path.getsize(processed_path)} bytes")
    
    # Cleanup
    for file in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, file))
    os.rmdir(test_dir)

if __name__ == "__main__":
    test_image_conversion() 