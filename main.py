import re
import requests
import telegram
from telegram.ext import Updater, CommandHandler

NETFLIX_API_URL = "https://www.netflix.com/api/shakti/{BUILD_IDENTIFIER}/pathEvaluator"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Netflix Image Scraper Bot! Send me a Netflix URL and I will fetch the poster image for you.")


def scrape_image(update, context):
    url = update.message.text.split()[1]

    # Extract the Netflix ID from the URL
    match = re.search(r"(?:\/title\/|\/watch\/)(\d+)", url)
    if match:
        netflix_id = match.group(1)
        build_identifier = get_build_identifier()
        if build_identifier:
            image_url = fetch_poster_image(netflix_id, build_identifier)
            if image_url:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
                return

    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't fetch the Netflix poster image from the provided URL.")


def get_build_identifier():
    response = requests.get("https://www.netflix.com")
    match = re.search(r"BUILD_IDENTIFIER\":\"([^ ]+)", response.text)
    if match:
        return match.group(1)

    return None


def fetch_poster_image(netflix_id, build_identifier):
    headers = {
        "Referer": f"https://www.netflix.com/title/{netflix_id}",
        "x-netflix-maturity": "com.netflix.maturity.violence_rating=5&com.netflix.maturity.rating=12&com.netflix.maturity.audience=4&com.netflix.maturity.isMature=false",
    }
    payload = {
        "withSize": "false",
        "materialize": "true",
    }
    api_url = NETFLIX_API_URL.replace("{BUILD_IDENTIFIER}", build_identifier)
    response = requests.post(api_url, headers=headers, params=payload)
    data = response.json()
    image_url = data.get("value", {}).get("image")
    return image_url


def main():
    # Initialize the Telegram bot
    updater = Updater(token='6206338404:AAHB41h-5oYWawSc9I7HtQZOQHox6JLibsg', use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    scrape_image_handler = CommandHandler('scrape_image', scrape_image)
    dispatcher.add_handler(scrape_image_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
