import os
import requests
from urllib.parse import urlsplit, unquote


def download_image(image_url, filepath, params=None):

    response = requests.get(image_url, params=params)
    response.raise_for_status()

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_file_format(image_url):
    image_path = urlsplit(image_url).path
    image_filename = os.path.basename(unquote(image_path))
    img_name, extension = os.path.splitext(image_filename)
    return extension.lower()


def tg_send_image(bot, tg_chat_id, image_path):
    with open(image_path, 'rb') as image:
        bot.send_photo(chat_id=tg_chat_id, photo=image)