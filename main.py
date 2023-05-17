import requests
from bs4 import BeautifulSoup
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def scrape_netflix_posters(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    posters = soup.find_all('img', {'class': 'boxart-image boxart-image-in-padded-container'})
    poster_urls = []

    for poster in posters:
        poster_url = poster['src']
        poster_urls.append(poster_url)

    return poster_urls

def download_posters(poster_urls, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_paths = []

    for i, url in enumerate(poster_urls):
        response = requests.get(url)
        file_name = f"poster_{i}.jpg"
        file_path = os.path.join(folder, file_name)

        with open(file_path, 'wb') as file:
            file.write(response.content)

        file_paths.append(file_path)

    return file_paths

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Netflix Poster Bot! Use /posters to get Netflix posters.")

def get_posters(update: Update, context: CallbackContext):
    netflix_url = 'https://www.netflix.com/browse/genre/839338'
    posters = scrape_netflix_posters(netflix_url)
    folder = 'netflix_posters'
    file_paths = download_posters(posters, folder)

    chat_id = update.message.chat_id
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            context.bot.send_photo(chat_id, photo=file)

def main():
    # Telegram bot token
    token = '6206338404:AAFQWpUemVDNSW6P1b6o90tfZoh--aG0qZA'

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("posters", get_posters))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
