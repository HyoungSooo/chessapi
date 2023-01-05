import os

def find_latest_file(folder):
    # Get a list of all the files in the folder
    files = os.listdir(folder)
    # Sort the list of files by modification time
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    # Get the most recent file
    latest_file = files[-1]
    # Return the full path of the file
    return os.path.join(folder, latest_file)