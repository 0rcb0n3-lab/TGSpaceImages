import argparse
import os
import time
import random
import telegram

from dotenv import load_dotenv
from download_images import tg_send_image
from telegram.error import NetworkError, TimedOut


def main():

    load_dotenv()

    parser = argparse.ArgumentParser(description="Telegram bot для автопостинга фото.")
    parser.add_argument(
        '--delay',
        default=4,
        type=float,
        help='Задержка/Интервал между постами в часах (по умолчанию 4 часа)'
    )
    parser.add_argument('--directory', default=os.getenv('IMAGE_DIRECTORY', 'Space_photos'),
                        help='Каталог с изображениями')
    args = parser.parse_args()
    delay_hours = args.delay
    directory = args.directory

    tgbot_token = os.environ['TGBOT_TOKEN']
    tgchat_id = os.environ['TG_CHAT_ID']
    post_delay = float(os.getenv('POST_DELAY_HOURS', delay_hours)) * 3600

    bot = telegram.Bot(token=tgbot_token)

    while True:
        images = [file for file in os.listdir(directory) if file.lower().endswith(('.jpg', '.png'))]

        if not images:
            print('В папке нет фотографий.')
            time.sleep(post_delay)
            continue

        random.shuffle(images)

        for filename in images:
            image_path = os.path.join(directory, filename)

            try:
                tg_send_image(bot, tgchat_id, image_path)

            except FileNotFoundError:
                print(f"Файл не найден: {image_path}")

            except NetworkError:
                print(f"(NetworkError) Ошибка отправки {filename}: Повтор через 30 с.")
                time.sleep(30)
                continue
            except TimedOut:
                print(f"(TimedOut) Ошибка отправки {filename}: Повтор через 30 с.")
                time.sleep(30)
                continue

            time.sleep(post_delay)


if __name__ == '__main__':
    main()
