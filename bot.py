import argparse
import os
import threading
import time

import telebot
import main_api
import schedule

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
text_remove_sign = '3️⃣Отписаться'
button_weather = types.KeyboardButton(text=text_weather)
button_sign = types.KeyboardButton(text=text_sign)
button_remove_sign = types.KeyboardButton(text=text_remove_sign)
keyboard.add(button_weather, button_sign, button_remove_sign)

current_sings = []


def send_for_signer():
    for chat_id in current_sings:
        path = main_api.current_path();
        if not main_api.has_current_day_graph(path):
            main_api.save_graphics_two_day(path)
        file = open(path, 'rb')
        bot.send_photo(chat_id, file)


schedule.every().day.at("8:00").do(send_for_signer)


def thread_sign():
    while 1:
        schedule.run_pending()
        time.sleep(1)


t = threading.Thread(target=thread_sign, name="Подписчики")
t.start()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    response = 'Привет, можешь получить погоду в Москве на два дня, либо подписаться на получение в 8 утра.'
    bot.send_message(message.chat.id, text=response, reply_markup=keyboard)


@bot.message_handler(regexp=text_weather)
def send_weather(message):
    path = main_api.current_path();
    if not main_api.has_current_day_graph(path):
        main_api.save_graphics_two_day(path)
    file = open(path, 'rb')
    bot.send_photo(message.chat.id, file)
    response = 'Будут еще пожелания?'
    bot.send_message(message.chat.id, text=response, reply_markup=keyboard)


@bot.message_handler(regexp=text_sign)
def send_sign(message):
    if message.chat.id in current_sings:
        response = 'Вы уже подписаны \U0001F602'
    else:
        current_sings.append(message.chat.id)
        response = 'Вы успешно подписались \U0000270C'
    bot.send_message(message.chat.id, text=response, reply_markup=keyboard)


@bot.message_handler(regexp=text_remove_sign)
def send_sign(message):
    if message.chat.id in current_sings:
        current_sings.remove(message.chat.id)
        response = 'Вы успешно отписались \U0001F614'
    else:
        response = 'А Вы и не подписаны \U0001F639'
    bot.send_message(message.chat.id, text=response, reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Я знаю только о погоде \U00002600 \U00002601')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Я знаю только о погоде \U00002600 \U00002601')


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





