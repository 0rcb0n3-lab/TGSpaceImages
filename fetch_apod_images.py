import os
import argparse
import requests

from dotenv import load_dotenv
from download_images import download_image, get_file_format


def fetch_apod_images(nasa_token, count):
    nasa_apod_api = 'https://api.nasa.gov/planetary/apod'
    params = {'count': count, 'api_key': nasa_token}
    response = requests.get(nasa_apod_api, params=params)
    response.raise_for_status()
    return response.json()


def download_apod_images(images, directory):

    for img_number, image in enumerate(images, start=1):
        if image.get('media_type') != 'image':
            continue

        link = image.get('url')
        extension = get_file_format(link)
        filename = f'nasa_{img_number}{extension}'
        filepath = os.path.join(directory, filename)

        download_image(link, filepath)


def main():
    load_dotenv()

    nasa_token = os.getenv('NASA_API_KEY')

    parser = argparse.ArgumentParser(
        description='Скачивает снимки APOD с NASA'
    )
    parser.add_argument('--nasa-token', default=nasa_token, help='API-ключ NASA')
    parser.add_argument('--count', type=int, default=6, help='Кол-во снимков (по умолчанию 6)')
    parser.add_argument('--directory', default=os.getenv('IMAGE_DIRECTORY', 'Space_photos'),
                        help='Каталог для сохранения изображений')
    args = parser.parse_args()

    
    if not args.nasa_token:
        raise RuntimeError('NASA_API_KEY не найден в .env / не передан через --nasa-token')

    images = fetch_apod_images(args.nasa_token, args.count)

    download_apod_images(images, args.directory)


if __name__ == '__main__':
    main()
