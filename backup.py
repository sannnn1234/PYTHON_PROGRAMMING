import os
import sys
import shutil
from datetime import datetime

def backup_files(source_dir, dest_dir):
    # Check if source exists
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    # Check if destination exists
    if not os.path.isdir(dest_dir):
        print(f"Error: Destination directory '{dest_dir}' does not exist.")
        return

    # List all files in source directory
    files = os.listdir(source_dir)
    
    if not files:
        print("No files found in source directory.")
        return

    for file_name in files:
        source_path = os.path.join(source_dir, file_name)

        # Skip if it's a directory
        if os.path.isdir(source_path):
            continue

        dest_path = os.path.join(dest_dir, file_name)

        # If file exists, add timestamp
        if os.path.exists(dest_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(file_name)
            new_file_name = f"{name}_{timestamp}{ext}"
            dest_path = os.path.join(dest_dir, new_file_name)
            print(f"File exists. Renamed to: {new_file_name}")

        # Copy file
        try:
            shutil.copy2(source_path, dest_path)
            print(f"Copied: {file_name}")
        except Exception as e:
            print(f"Failed to copy {file_name}: {e}")


if __name__ == "__main__":
    # Require exactly 2 arguments
    if len(sys.argv) != 3:
        print("Usage: python backup.py <source_dir> <destination_dir>")
        sys.exit(1)

    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]

    backup_files(source_directory, destination_directory)