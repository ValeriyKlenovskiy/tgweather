import telebot
from telebot import types
import requests

bot = telebot.TeleBot('5494607822:AAF95G3dRyeWmFr4Z7pJsvWekhCMQqCzI7c')


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    weather = types.KeyboardButton('Хочу узнать погоду в Минске')
    markup.add(weather)
    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler()
def get_user_text(message):
    if message.text == 'Хочу узнать погоду в Минске':
        appid = '8daa6b89a01831f95f8337db4a9119a8'
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
        city = 'Minsk'
        res = requests.get(url.format(city)).json()
        city_info = {
            'temp': res['main']['temp'],
            'weather': res['weather'][0]['description'],
            'wind': res['wind']['speed']
        }
        weather_now = f"Температура: {city_info['temp']} °C\nСкорость ветра: {city_info['wind']} м/с\nОписание: {city_info['weather']}"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        sps = types.KeyboardButton('Спасибо')
        markup.add(sps)
        bot.send_message(message.chat.id, weather_now, reply_markup=markup)
    elif message.text == 'Спасибо':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        start = types.KeyboardButton('/start')
        markup.add(start)
        bot.send_message(message.chat.id, 'Не за что', reply_markup=markup)


bot.polling(none_stop=True)
