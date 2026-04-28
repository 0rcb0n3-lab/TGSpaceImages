import os
import requests
from urllib.parse import urlsplit, unquote


def download_image(image_url, filepath):

    response = requests.get(image_url)
    response.raise_for_status()

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_file_format(image_url):
    image_path = urlsplit(image_url).path
    image_filename = os.path.basename(unquote(image_path))
    img_name, extension = os.path.splitext(image_filename)
    return extension.lower()
