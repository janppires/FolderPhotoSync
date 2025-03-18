# FolderPhotoSync
A Python script to synchronize photo timestamps with the date extracted from their parent folder names (e.g., `2022-03-17`). Updates EXIF metadata (DateTime, DateTimeOriginal, DateTimeDigitized) and filesystem timestamps (modification and access times) to midday of the folder date. Ideal for organizing photo collections on NAS devices like Synology, with support for JPEG and PNG files. Enhance your photo archiving workflow with this automated solution!

# Table of Contents
- Feature`s
- Prerequisites
- Installation
- Usage
- Configuration
- Contributing

# Features
- Extracts the date from parent folder names (e.g., `2022-03-17`).
- Updates EXIF metadata (DateTime, DateTimeOriginal, DateTimeDigitized) to midday (12:00:00) of the folder date.
- Sets filesystem modification and access timestamps, and creation time where supported, to the same midday date for both images and videos.
- Preserves folder structure while copying photos and videos to a new destination.
- Supports JPEG, PNG, and MP4 file formats.
- Compatible with NAS setups (e.g., Synology) mounted on macOS.
- Note: Creation time (`birthtime`) on macOS is not updated directly by this script. See Troubleshooting for workarounds.

# Prerequisites
- Python 3.x: Ensure Python is installed on your system.
- Libraries:
  - `Pillow`: For image processing and EXIF manipulation.
  - `piexif`: For handling EXIF data.
  - Install them via pip:
```bash
pip install Pillow piexif
```
- Optional Tools (for creation time updates):
  - `exiftool`: For setting all timestamps, including creation time. Install via Homebrew on macOS:
```bash
brew install exiftool
```
  - `SetFile`: Part of Xcode Command Line Tools for macOS (install with `xcode-select --install`).

# Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/FolderPhotoSync.git
cd FolderPhotoSync
```
2. Install the required Python libraries:
```bash
pip install -r requirements.txt
```
(Create a `requirements.txt file with `Pillow` and `piexif if not already included.)
3. Ensure your NAS is mounted and accessible (e.g., `/Volumes/home/Temporary`).

# Usage
1. Update the script with your source and destination paths in the `root_dir` and `dest_dir` variables:

```python
root_dir = "/Volumes/home/Temporary/2022"
dest_dir = "/Volumes/home/Temporary/2022_Updated"
```
2. Run the script:
```bash
python folderphotosync.py
```
3. The script will:
- Copy photos from the source directory to the destination.
- Update EXIF and filesystem timestamps based on the parent folder date.

# Example Folder Structure
```
2022/
├── 2022-03-17/
│   ├── photo1.jpg
│   ├── photo2.png
│   └── video1.mp4
├── 2022-03-18-First Day/
│   ├── image3.jpg
│   └── video2.mp4
2022_Updated/
├── 2022-03-17/
│   ├── photo1.jpg (timestamps set to 2022-03-17 12:00:00)
│   ├── photo2.png (timestamps set to 2022-03-17 12:00:00)
│   └── video1.mp4 (timestamps set to 2022-03-17 12:00:00)
├── 2022-03-18-First Day/
│   ├── image3.jpg (timestamps set to 2022-03-18 12:00:00)
│   └── video2.mp4 (timestamps set to 2022-03-18 12:00:00)
```
# Configuration
- Modify image_extensions in the script to support additional file types (e.g., .gif, .bmp).
- Adjust the timestamp logic in extract_date_from_folder if you use a different folder naming convention.

# Contributing
Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch (git checkout -b feature-name).
3. Commit your changes (git commit -m "Add feature").
4. Push to the branch (git push origin feature-name).
5. Open a Pull Request.

Report issues or suggest enhancements via the Issues tab.

