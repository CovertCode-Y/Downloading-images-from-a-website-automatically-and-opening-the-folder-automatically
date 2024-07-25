import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import subprocess
import re

def sanitize_filename(filename):
    # Remove invalid characters and replace spaces with underscores
    return re.sub(r'[^\w\-_\. ]', '_', filename).replace(' ', '_')

def download_images(url, folder_name='downloaded_images'):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Send a GET request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all img tags
    img_tags = soup.find_all('img')

    # Download each image
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            # Make the URL absolute by joining it with the base URL
            img_url = urljoin(url, img_url)
            
            # Parse the URL and get the path
            parsed_url = urlparse(img_url)
            path = parsed_url.path
            
            # Get the file name from the path and sanitize it
            file_name = sanitize_filename(os.path.basename(path))
            
            # If the filename is empty after sanitization, use a default name
            if not file_name:
                file_name = 'image_' + sanitize_filename(parsed_url.query) + '.jpg'
            
            # Ensure the filename has an extension
            if not os.path.splitext(file_name)[1]:
                file_name += '.jpg'
            
            # Create the full file path
            file_path = os.path.join(folder_name, file_name)
            
            try:
                # Download the image
                img_data = requests.get(img_url).content
                with open(file_path, 'wb') as file:
                    file.write(img_data)
                print(f"Downloaded: {file_path}")
            except Exception as e:
                print(f"Error downloading {img_url}: {str(e)}")

    print("All images downloaded successfully!")

    # Open the folder
    if os.name == 'nt':  # For Windows
        os.startfile(folder_name)
    elif os.name == 'posix':  # For macOS and Linux
        subprocess.call(('open', folder_name))

# Use the function
url = "https://www.kikar.co.il/"
download_images(url)