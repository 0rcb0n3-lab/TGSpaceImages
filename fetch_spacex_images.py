import os
import argparse
import requests

from dotenv import load_dotenv
from download_images import download_image


def fetch_spacex_recent_launch(launch_id, directory):

    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()

    launch_spec = response.json()
    links = launch_spec.get("links", {}).get("flickr", {}).get("original", [])

    if not links:
        print("Изображения не найдены в данных последнего запуска.")
        return

    for img_number, img_url in enumerate(links, start=1):
        if not img_url:
            continue

        filename = f'spacex_{img_number}.jpg'
        filepath = os.path.join(directory, filename)
        download_image(img_url, filepath)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Скачивает изображения запуска SpaceX по ID'
    )
    parser.add_argument(
        '--launch-id',
        default='5eb87d47ffd86e000604b38a',
        help='ID запуска (по умолчанию: 5eb87d47ffd86e000604b38a, '
             'указать "--launch-id latest" для актуального)'
    )
    parser.add_argument('--directory', default=os.getenv('IMAGE_DIRECTORY', 'Space_photos'),
                        help='Каталог для сохранения изображений')
    args = parser.parse_args()

    fetch_spacex_recent_launch(args.launch_id, args.directory)


if __name__ == '__main__':
    main()
