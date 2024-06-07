import os
import shutil
from datetime import datetime
from tqdm import tqdm

def rearrange_videos_by_date(folder_path, output_folder):
    # List all files in the directory
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Get the file modification times and sort the files by date
    files_with_dates = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        modification_time = os.path.getmtime(file_path)
        files_with_dates.append((file, modification_time))
    
    # Sort files by modification date
    files_with_dates.sort(key=lambda x: x[1])
    
    # Create a new folder to store sorted videos
    sorted_folder = os.path.join(output_folder, "sorted_videos")
    if not os.path.exists(sorted_folder):
        os.makedirs(sorted_folder)
    
    # Copy sorted files to the new folder with a progress bar
    for i, (file, date) in enumerate(tqdm(files_with_dates, desc="Rearranging videos", unit="file")):
        original_path = os.path.join(folder_path, file)
        new_file_name = f"{i+1:03d}_{file}"  # Prepend a number to the filename
        new_file_path = os.path.join(sorted_folder, new_file_name)
        shutil.copy2(original_path, new_file_path)
    
    print(f"Videos have been rearranged and copied to: {sorted_folder}")

# Example usage
folder_path = input('Video input path: ')
# folder_path = '/Desktop'
output_path = input('Video output path: ')
rearrange_videos_by_date(folder_path, output_path)
