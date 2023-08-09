import re
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from youtube_transcript_api import YouTubeTranscriptApi

BOT_TOKEN = 'Your Bot token'


def extract_video_id(url):
    regex = r"(?:\?v=|\/+|)([0-9A-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None


def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = ''

    for i in transcript:
        t = i['text']
        if t != '[Music]':
            text += t + ' '

    return text

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to the bot! Paste a YouTube link here and I will return the video's subtitles.")

def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="To use this bot, paste a YouTube link. If you encounter any issues, please contact the developer @CaptainLightyear.")

def handle_message(update, context):
    print("Bot has started.")
    url = update.message.text

    if 'youtube.com' in url or 'youtu.be' in url:
        print("Processing link.")
        video_id = extract_video_id(url)

        subtitle = get_transcript(video_id)

        file = open('subtitle.txt', 'w')
        file.write(subtitle)
        file.close()

        print("Sending file.")
        context.bot.send_document(chat_id=update.message.chat_id, document=open('subtitle.txt', 'rb'))

        print("Deleting file.")
        os.remove('subtitle.txt')

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

updater.start_polling()
updater.idle()
