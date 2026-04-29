import os
import random
import telegram
from dotenv import load_dotenv
from download_images import tg_send_image


def main():
    load_dotenv()

    tgbot_token = os.environ['TGBOT_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']

    bot = telegram.Bot(token=tgbot_token)

    directory = 'Space_photos'
    images = [file for file in os.listdir(directory) if file.lower().endswith(('.jpg', '.png'))]

    random_image = random.choice(images)
    image_path = os.path.join(directory, random_image)

    tg_send_image(bot, tg_chat_id, image_path)


if __name__ == '__main__':
    main()
