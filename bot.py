import argparse
import os
import telebot

from telebot import types
from flask import Flask, request

API_TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(API_TOKEN)

server = Flask(__name__)
TELEBOT_URL = 'telebot_webhook/'
BASE_URL = 'https://weather-bot-tony.herokuapp.com/'

keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
text_weather = '1️⃣Получить погоду'
text_sign = '2️⃣Подписаться'


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    response = 'Привет, можешь получить погоду на два дня, либо подписаться на получение в 8 утра.'
    button_phone = types.KeyboardButton(text=text_weather)
    button_geo = types.KeyboardButton(text=text_sign)
    keyboard.add(button_phone, button_geo)
    bot.send_message(text=response, reply_markup=keyboard)


@bot.message_handler(regexp=text_weather)
def send_weather(message):
    response = 'Хочешь погоду???'
    bot.send_message(text=response, reply_markup=keyboard)


@bot.message_handler(regexp=text_sign)
def send_sign(message):
    response = 'Пока нельзя подписаться \U0001F614'
    bot.send_message(text=response, reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Чё-то я не понял')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Чё-то я не понял')


@server.route('/' + TELEBOT_URL + API_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BASE_URL + TELEBOT_URL + API_TOKEN)
    return "!", 200


parser = argparse.ArgumentParser(description='Run the bot')
parser.add_argument('--poll', action='store_true')
args = parser.parse_args()

if args.poll:
    bot.remove_webhook()
    bot.polling()
else:
    # webhook should be set first
    webhook()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))





