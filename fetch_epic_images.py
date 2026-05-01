import argparse
import os
import requests

from datetime import datetime
from urllib.parse import urlencode
from dotenv import load_dotenv
from download_images import download_image


def fetch_epic_images(nasa_token, img_count):
    nasa_epic_api = 'https://api.nasa.gov/EPIC/api/natural'
    params = {'api_key': nasa_token}
    response = requests.get(nasa_epic_api, params=params)
    response.raise_for_status()

    image_spec = response.json()
    img_urls = []

    for item in image_spec[:img_count]:
        date = datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S')
        name = item['image']
        raw_link = f'https://api.nasa.gov/EPIC/archive/natural/{date:%Y/%m/%d}/png/{name}.png'
        img_urls.append((raw_link, name, params))

    return img_urls


def download_epic_images(img_urls, directory):

    for img_number, (link, name, params) in enumerate(img_urls, start=1):
        filename = f'epic_{img_number}.png'
        filepath = os.path.join(directory, filename)
        download_image(link, filepath, params=params)


def main():
    load_dotenv()

    nasa_token = os.getenv('NASA_API_KEY')

    parser = argparse.ArgumentParser(
        description='Скачивает снимки EPIC с NASA'
    )
    parser.add_argument('--nasa-token', default=nasa_token, help='API-ключ NASA')
    parser.add_argument('--count', type=int, default=3, help='Кол-во снимков (по умолчанию 3)')
    parser.add_argument('--directory', default=os.getenv('IMAGE_DIRECTORY', 'Space_photos'),
                        help='Каталог для сохранения изображений')
    args = parser.parse_args()

    
    if not args.nasa_token:
        raise RuntimeError('NASA_API_KEY не найден в .env / не передан через --nasa-token')

    links = fetch_epic_images(args.nasa_token, args.count)
    download_epic_images(links, args.directory)


if __name__ == '__main__':
    main()
