import requests
from bs4 import BeautifulSoup
import telegram
from telegram.ext import Updater, CommandHandler


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Netflix Data Extractor Bot! Send me a Netflix URL and I will scrape the data for you.")


def scrape_data(update, context):
    url = update.message.text.split()[1]

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    o = {}
    e = {}
    d = {}
    m = {}
    c = {}
    l = []

    o["name"] = soup.find("h1", {"class": "title-title"}).text

    o["seasons"] = soup.find("span", {"class": "duration"}).text

    o["about"] = soup.find("div", {"class": "hook-text"}).text

    episodes_container = soup.find("ol", {"class": "episodes-container"})
    if episodes_container:
        episodes = episodes_container.find_all("li")
        for i in range(0, len(episodes)):
            e["episode-title"] = episodes[i].find("h3", {"class": "episode-title"}).text
            e["episode-description"] = episodes[i].find("p", {"class": "episode-synopsis"}).text
            l.append(e)
            e = {}

    genres = soup.find_all("span", {"class": "item-genres"})
    for x in range(0, len(genres)):
        d["genre"] = genres[x].text.replace(",", "")
        l.append(d)
        d = {}

    mood = soup.find_all("span", {"class": "item-mood-tag"})
    for y in range(0, len(mood)):
        m["mood"] = mood[y].text.replace(",", "")
        l.append(m)
        m = {}

    o["facebook"] = soup.find("a", {"data-uia": "social-link-facebook"}).get("href")
    o["twitter"] = soup.find("a", {"data-uia": "social-link-twitter"}).get("href")
    o["instagram"] = soup.find("a", {"data-uia": "social-link-instagram"}).get("href")

    cast = soup.find_all("span", {"class": "item-cast"})
    for t in range(0, len(cast)):
        c["cast"] = cast[t].text
        l.append(c)
        c = {}

    l.append(o)

    # Send the scraped data as a reply
    context.bot.send_message(chat_id=update.effective_chat.id, text=str(l))


def main():
    # Initialize the Telegram bot
    updater = Updater(token='6206338404:AAFQWpUemVDNSW6P1b6o90tfZoh--aG0qZA', use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    scrape_data_handler = CommandHandler('scrape', scrape_data)
    dispatcher.add_handler(scrape_data_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
