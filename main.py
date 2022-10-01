import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler
import os
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# working
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_qry = update.message.text
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=update)
    all_updates = update.to_dict()

    if "keekey" in bot_qry.casefold() or "what" in bot_qry.casefold():
        if "reply_to_message" in all_updates["message"].keys():

            import requests
            text = all_updates["message"]["reply_to_message"]["text"]
            url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
            to_trans = text.replace(" ","%20")
            payload = f"q={to_trans}&target=dv&source=en&format=text"
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "application/gzip",
                "X-RapidAPI-Key": "",
                "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            print(response.json()["data"]["translations"][0]["translatedText"])
            translated = response.json()["data"]["translations"][0]["translatedText"]


            await context.bot.send_message(chat_id=update.effective_chat.id, text=translated)


# working part
async def commd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Add me in any group. Make me an Admin & I Will send you viewable tiktoks")


if __name__ == '__main__':
    token = "5510111232:AAGMCdx0i0Ehet8RUgqv_VVU2FXrJ-EsZJ8"
    application = ApplicationBuilder().token(token).build()

    commands = CommandHandler('start', commd)
    links = MessageHandler(filters.TEXT, start)
    # on different commands - answer in Telegram
    application.add_handler(commands)
    application.add_handler(links)

    application.run_polling()
