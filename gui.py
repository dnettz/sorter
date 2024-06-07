import os
import shutil
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from tqdm import tqdm

def rearrange_files_by_date(source_folder, destination_folder, progress_bar, progress_label):
    # List all files in the directory
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    # Get the file modification times and sort the files by date
    files_with_dates = []
    for file in files:
        file_path = os.path.join(source_folder, file)
        modification_time = os.path.getmtime(file_path)
        files_with_dates.append((file, modification_time))
    
    # Sort files by modification date
    files_with_dates.sort(key=lambda x: x[1])
    
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Initialize the progress bar
    total_files = len(files_with_dates)
    progress_bar['maximum'] = total_files
    
    # Copy sorted files to the destination folder with a progress bar
    for i, (file, date) in enumerate(files_with_dates):
        original_path = os.path.join(source_folder, file)
        new_file_name = f"{i+1:03d}_{file}"  # Prepend a number to the filename
        new_file_path = os.path.join(destination_folder, new_file_name)
        shutil.copy2(original_path, new_file_path)
        
        # Update the progress bar and percentage label
        progress_bar['value'] = i + 1
        percentage = ((i + 1) / total_files) * 100
        progress_label.config(text=f"{percentage:.2f}%")
        progress_bar.update_idletasks()
    
    messagebox.showinfo("Completed", f"Files have been rearranged and copied to: {destination_folder}")

def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, END)
    entry.insert(0, folder_selected)

def start_rearrangement(source_entry, destination_entry, progress_bar, progress_label):
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    if not source_folder:
        messagebox.showwarning("Input Error", "Please select a source folder.")
        return
    if not destination_folder:
        messagebox.showwarning("Input Error", "Please select a destination folder.")
        return
    rearrange_files_by_date(source_folder, destination_folder, progress_bar, progress_label)

def create_gui():
    root = ttk.Window(themename="flatly")
    root.title("File Rearranger")
    
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=BOTH, expand=True)
    
    source_label = ttk.Label(frame, text="Select Source Folder:")
    source_label.pack(pady=5)
    
    source_entry = ttk.Entry(frame, width=50)
    source_entry.pack(pady=5)
    
    source_browse_button = ttk.Button(frame, text="Browse", command=lambda: browse_folder(source_entry))
    source_browse_button.pack(pady=5)
    
    destination_label = ttk.Label(frame, text="Select Destination Folder:")
    destination_label.pack(pady=5)
    
    destination_entry = ttk.Entry(frame, width=50)
    destination_entry.pack(pady=5)
    
    destination_browse_button = ttk.Button(frame, text="Browse", command=lambda: browse_folder(destination_entry))
    destination_browse_button.pack(pady=5)
    
    progress_bar = ttk.Progressbar(frame, orient=HORIZONTAL, length=300, mode='determinate')
    progress_bar.pack(pady=5)
    
    progress_label = ttk.Label(frame, text="0.00%")
    progress_label.pack(pady=5)
    
    start_button = ttk.Button(frame, text="Start", command=lambda: start_rearrangement(source_entry, destination_entry, progress_bar, progress_label))
    start_button.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
