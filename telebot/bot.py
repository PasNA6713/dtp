import os
import json
import requests

import telebot
from dotenv import load_dotenv
from loguru import logger


load_dotenv(".env")

bot = telebot.TeleBot(os.getenv("MY_KEY"))
BACKEND = os.getenv("BACKEND_URL")


def catch_backend_off(func):
    ''' 
    Декоратор для определения ошибок доступа к беку.
    Использовать ДО декоратора catch_user.
    '''
    def decor(message):
        try: 
            func(message)
        except requests.exceptions.ConnectionError:
            bot.reply_to(message, 'Извините, на этом сервер все...')
    return decor


def catch_user(func):
    ''' 
    Декоратор для определения пользователя.
    Handler должен принимать message, user. 
    Использовать ПОСЛЕ декоратора telebot'а
    '''
    def decor(message):
        from_user = message.from_user
        user = {
            'id': from_user.id,
            'firstname': from_user.first_name,
            'lastname': from_user.last_name
        }
        return func(message, user)
    return decor


@bot.message_handler(content_types=['location'])
@catch_backend_off
@catch_user
def location_processing(message, user):
    ''' Принимаем геолокацию '''
    location = message.location
    # bot.reply_to(message, 'Ваше заявление принято, оператор свяжется с вами в ближайшее время')
    

@bot.message_handler(content_types=['venue'])
@catch_backend_off
@catch_user
def venue_processing(message, user):
    ''' Принимаем место '''
    place = message.venue
    address = place.address
    location = place.location
    title = place.title
    # bot.reply_to(message, 'Ваше заявление принято, оператор свяжется с вами в ближайшее время')


@bot.message_handler(content_types=['voice'])
@catch_backend_off
@catch_user
def voice_processing(message, user):
    ''' Принимаем голосовуху '''
    file_info = bot.get_file(message.voice.file_id)
    to_send = bot.download_file(file_info.file_path)
    requests.post(
        f'{BACKEND}create/voice/',
        files={
            'file': to_send
        },
        data={
            'filename': 'message.ogg'
        }
    )
    bot.reply_to(message, 'Ваше заявление принято, оператор свяжется с вами в ближайшее время')


bot.polling()