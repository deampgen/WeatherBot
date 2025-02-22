import telebot
from config import TOKEN
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
bot = telebot.TeleBot(TOKEN)

ua = UserAgent(os='Linux')

def find_weather(city=None):
    user_agent = ua.random
    if city:
        url = f'https://yandex.ru/pogoda/{city}'
    else:
        url = f'https://yandex.ru/pogoda'
    try:
        response = requests.get(url, headers={'User-Agent': user_agent})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            temp_element = soup.find('span', class_='temp__value temp__value_with-unit')
            if temp_element:
                temp = temp_element.text.strip()
            else:
                temp = 'N/A'
            condition_element = soup.find('div', class_='link__condition day-anchor i-bem')
            if condition_element:
                condition = condition_element.text.strip()
            else:
                condition = 'N/A'
            return temp, condition
        else:
            print('error, connection lost.')
    except Exception as e:
        print(f'Error: {e}')



@bot.message_handler(commands=['weather'])
def weather(message):
    chat_id = message.chat.id
    text = message.text.strip()
    city_name = text.replace('/weather', '').strip().lower().replace(' ', '-') or None
    temp, condition = find_weather(city_name)
    if temp != 'N/A' and condition != 'N/A':
        bot.send_message(chat_id=chat_id, text=f'temp: {temp}°\ncondition: {condition}')
    else:
        bot.send_message(chat_id=chat_id, text=f'no weather available')

@bot.message_handler(commands=['start'])
def welcome_message(message):
    chat_id = message.chat.id

    bot.send_message(chat_id=chat_id,
                     text = 'Hello, iam your helper to find the weather in your city!!\nchoose which buttons do you need down below!\nto find your weather in your city write command /weather \n do you need some help? write /help command'

                     )

@bot.message_handler(commands=['help'])
def help_message(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text = 'what help do you need?\nif you dont know how to find your city weather\nyou need to write the command /weather <city> to find out\nto write admin you need to write /admin command'
    )
@bot.message_handler(commands=['admin'])
def admin_message(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text = 'you probably thought you can write our admin?\nfuck no its not possible <a href="https://t.me/PrgmPy">fuck you</a>',
        parse_mode='HTML'
    )





bot.infinity_polling()