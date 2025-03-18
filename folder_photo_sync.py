import os
import shutil
import datetime
import subprocess
from pathlib import Path
from PIL import Image as PILImage
import piexif

# Define the root directory of your photos and videos (replace with your NAS path)
root_dir = "/Volumes/home/Photos/OtherPhotos/Some Photos"

# Define the destination directory for copied files
dest_dir = "/Volumes/home/Photos/OtherPhotos/Some Photos - Update"

# Supported file extensions
supported_extensions = ('.jpg', '.jpeg', '.png', '.mp4')

# Function to extract date from folder name
def extract_date_from_folder(folder_name):
    # Split the folder name by '-' and take the first part (YYYY-MM-DD)
    date_part = folder_name.split('-', 3)[:3]
    date_str = '-'.join(date_part)
    try:
        # Parse the date
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        # Set the time to midday (12:00:00)
        date = date.replace(hour=12, minute=0, second=0, microsecond=0)
        return date
    except ValueError:
        print(f"Could not parse date from folder name: {folder_name}")
        return None

# Function to update or add EXIF timestamp for images
def update_exif_timestamp(image_path, new_timestamp):
    try:
        # Check if the file exists and is readable
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Open the image with Pillow
        with PILImage.open(image_path) as img:
            # Verify the image can be processed
            img.verify()
        
        # Format the timestamp for EXIF (YYYY:MM:DD HH:MM:SS)
        exif_date_str = new_timestamp.strftime('%Y:%m:%d %H:%M:%S').encode('utf-8')
        
        # Load existing EXIF data, if any
        exif_dict = {'0th': {}, 'Exif': {}, 'GPS': {}, 'Interop': {}, '1st': {}, 'thumbnail': None}
        try:
            exif_bytes = img.info.get('exif', None)
            if exif_bytes:
                exif_dict = piexif.load(exif_bytes)
        except piexif.InvalidImageDataError as e:
            print(f"Invalid EXIF data in {image_path}. Creating new EXIF data. Error: {e}")

        # Update the EXIF fields for DateTime, DateTimeOriginal, and DateTimeDigitized
        exif_dict['0th'][piexif.ImageIFD.DateTime] = exif_date_str
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = exif_date_str
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = exif_date_str

        # Convert the EXIF dictionary to bytes
        exif_bytes = piexif.dump(exif_dict)

        # Save the image with the updated EXIF data
        with PILImage.open(image_path) as img:
            img.save(image_path, 'JPEG' if image_path.lower().endswith(('.jpg', '.jpeg')) else img.format, exif=exif_bytes, quality='keep')
        
        print(f"Updated EXIF timestamp for {image_path} to {exif_date_str.decode('utf-8')}")
        return True
    except FileNotFoundError as e:
        print(f"File error for {image_path}: {e}")
        return False
    except PILImage.DecompressionBombError:
        print(f"Decompression bomb error for {image_path}. Skipping due to potential corruption or large size.")
        return False
    except Exception as e:
        print(f"Failed to update EXIF timestamp for {image_path}: {e}")
        return False

# Function to update filesystem timestamps for all files
def update_filesystem_timestamps(file_path, new_timestamp):
    try:
        # Format the timestamp for exiftool
        timestamp_str = new_timestamp.strftime('%Y:%m:%d %H:%M:%S')
        
        # Use exiftool to set all timestamps (creation, modification, and QuickTime metadata for videos)
        subprocess.run([
            'exiftool',
            '-overwrite_original',
            f'-CreateDate={timestamp_str}',
            f'-ModifyDate={timestamp_str}',
            f'-FileCreateDate={timestamp_str}',
            f'-FileModifyDate={timestamp_str}',
            file_path
        ], check=True)
        
        print(f"Updated all timestamps (filesystem and metadata) for {file_path} to {timestamp_str}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to update timestamps with exiftool for {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Failed to update filesystem timestamps for {file_path}: {e}")
        return False

# Function to copy file and update its timestamps
def copy_and_update_timestamps(src_path, dest_path, new_timestamp):
    # Create the destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Copy the file
    shutil.copy2(src_path, dest_path)
    
    # Update timestamps based on file type
    if dest_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        if update_exif_timestamp(dest_path, new_timestamp):
            update_filesystem_timestamps(dest_path, new_timestamp)
    elif dest_path.lower().endswith('.mp4'):
        update_filesystem_timestamps(dest_path, new_timestamp)
    else:
        print(f"Unsupported file type for {dest_path}. Skipping timestamp update.")

# Main script
def process_files():
    # Walk through the root directory
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        
        # Skip if it's not a directory
        if not os.path.isdir(folder_path):
            continue
        
        # Extract the date from the folder name
        new_timestamp = extract_date_from_folder(folder_name)
        if new_timestamp is None:
            continue
        
        # Create the corresponding destination folder
        dest_folder = os.path.join(dest_dir, folder_name)
        
        # Walk through the folder to find supported files
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Check if the file is supported
                if file.lower().endswith(supported_extensions):
                    src_file = os.path.join(root, file)
                    # Construct the destination path
                    relative_path = os.path.relpath(src_file, folder_path)
                    dest_file = os.path.join(dest_folder, relative_path)
                    # Copy the file and update its timestamps
                    copy_and_update_timestamps(src_file, dest_file, new_timestamp)

if __name__ == "__main__":
    # Create the destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    # Run the script
    process_files()
    print("Processing complete!")