import requests
from bs4 import BeautifulSoup
import telegram
from telegram.ext import Updater, CommandHandler


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Netflix Image Scraper Bot! Send me a Netflix URL and I will scrape the poster image for you.")


def scrape_image(update, context):
    url = update.message.text.split()[1]

    # Send a GET request to the Netflix URL and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the image tag in the HTML
    image_tag = soup.find('img', {'class': 'poster'})

    if image_tag:
        image_url = image_tag['src']

        # Send the image as a reply
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find the Netflix poster image on the provided URL.")


def main():
    # Initialize the Telegram bot
    updater = Updater(token='6206338404:AAFQWpUemVDNSW6P1b6o90tfZoh--aG0qZA', use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    scrape_image_handler = CommandHandler('scrape', scrape_image)
    dispatcher.add_handler(scrape_image_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
