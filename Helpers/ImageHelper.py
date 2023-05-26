import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.responses import FileResponse
from datetime import datetime





# Function to save the image to disk or file storage system
def save_image_to_disk(id, image_data):
    # Specify the directory where you want to save the images
    save_directory = '../map/'.encode()
    currentDate = datetime.now()
    # Create the save directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    filename = 'map'+str(currentDate)
    # Construct the full file path
    file_path = os.path.join(save_directory, filename.encode())

    if os.path.exists(file_path):
        # Serve the image to the user
        return FileResponse(file_path.decode())
    # Save the image data to the file
    with open(file_path, 'wb') as file:
        file.write(image_data.encode('utf-8'))
    return file_path
def get_image_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            image_data = file.read()
        return image_data
    except IOError:
        print("Error: Could not read file:", file_path)
        return None